
import os
import sqlite3
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from groq import Groq
import prompts
import db

# Load .env file automatically (works locally; on Render use env vars panel)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on system env vars

app = FastAPI(title="Founder's Portfolio Engine")

# 1. Initialize DB
db.init_db()

# Enable CORS for the Mobile PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ThoughtInput(BaseModel):
    raw_thought: str

class MasteryInput(BaseModel):
    text: str

class JournalInput(BaseModel):
    content: str

def get_ai_response(prompt: str):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompts.SYSTEM_PROMPT},
                 {"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

@app.post("/generate")
async def generate_brief(input_data: ThoughtInput):
    thought = input_data.raw_thought
    mini = get_ai_response(prompts.MINI_INSIGHT_PROMPT.replace("{raw_input}", thought))
    if not mini: mini = f"Venture concept focusing on {thought}."
    
    full_brief = {
        "s1": get_ai_response(prompts.MARKET_INTEL_PROMPT.replace("{raw_input}", thought)),
        "s2": get_ai_response(prompts.AI_ROADMAP_PROMPT.replace("{raw_input}", thought)),
        "s3": get_ai_response(prompts.STANFORD_SPIKE_PROMPT.replace("{raw_input}", thought)),
        "s4": get_ai_response(prompts.COMMUNICATION_LAB_PROMPT.replace("{raw_input}", thought)),
        "s5": get_ai_response(prompts.NEWS_INTELLIGENCE_PROMPT.replace("{raw_input}", thought)),
        "s6": get_ai_response(prompts.DEEP_RESEARCH_PROMPT.replace("{raw_input}", thought))
    }
    db.save_thought(thought, mini, json.dumps(full_brief))
    return {"mini_insight": mini, "full_brief": full_brief}

@app.post("/refine-english")
async def refine_english(input_data: MasteryInput):
    text = input_data.text
    response = get_ai_response(prompts.STANFORD_MASTERY_PROMPT.replace("{raw_input}", text))
    return {"analysis": response}

@app.post("/save-journal")
async def save_journal(input_data: JournalInput):
    db.save_journal(input_data.content)
    return {"status": "success"}

@app.get("/get-journal")
async def get_journal():
    rows = db.get_all_journal()
    return [{"content": r[0], "date": r[1]} for r in rows]

@app.get("/vault")
async def get_vault():
    rows = db.get_all_thoughts()
    vault_data = []
    for r in rows:
        try:
            fb = json.loads(r[3])
        except:
            fb = {}
        vault_data.append({"id": r[0], "raw_input": r[1], "mini_insight": r[2], "full_brief": fb, "created_at": r[4]})
    return vault_data

class MemoryTaskInput(BaseModel):
    text: str
    manual: bool = False

class MemoryTaskComplete(BaseModel):
    task_id: int

class ReadingNoteInput(BaseModel):
    thought_id: int = 0
    content: str

def calculate_next_revision(current_step: int, last_revision_iso: str | None = None):
    from datetime import datetime, timedelta
    now = datetime.now()
    if current_step == 0:
        return (now + timedelta(days=1)).isoformat()
    elif current_step == 1:
        return (now + timedelta(days=4)).isoformat()
    elif current_step == 2:
        return (now + timedelta(days=7)).isoformat()
    return None

@app.post("/explain")
async def explain_text(input_data: MasteryInput):
    text = input_data.text
    response = get_ai_response(prompts.EXPLANATION_PROMPT.replace("{raw_input}", text))
    
    # Parse explanation and example from AI response
    explanation = ""
    example = ""
    if response:
        lines = response.split("\n")
        for line in lines:
            if line.upper().startswith("EXPLANATION:"):
                explanation = line.split(":", 1)[1].strip()
            if line.upper().startswith("EXAMPLE:"):
                example = line.split(":", 1)[1].strip()
    
    if not explanation: explanation = f"Explanation for: {text}"
    
    return {"explanation": explanation, "example": example}

@app.post("/memory-tasks/add")
async def add_memory_task(input_data: MemoryTaskInput):
    explanation = ""
    example = ""
    
    if not input_data.manual:
        # If not manual, we auto-explain
        resp = await explain_text(MasteryInput(text=input_data.text))
        explanation = resp["explanation"]
        example = resp["example"]
    else:
        # Manual might just be a word, we'll still get a quick explanation
        resp = await explain_text(MasteryInput(text=input_data.text))
        explanation = resp["explanation"]
        example = resp["example"]

    next_rev = calculate_next_revision(0)
    db.save_memory_task(input_data.text, explanation, example, next_rev)
    return {"status": "success", "explanation": explanation, "example": example}

@app.get("/memory-tasks/due")
async def get_due_tasks():
    from datetime import datetime
    now = datetime.now().isoformat()
    rows = db.get_due_memory_tasks(now)
    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "text": r[1],
            "explanation": r[2],
            "example": r[3],
            "next_revision": r[4],
            "step": r[5]
        })
    return tasks

@app.post("/memory-tasks/complete")
async def complete_memory_task(input_data: MemoryTaskComplete):
    # Fetch task to get current step
    all_tasks = db.get_all_memory_tasks()
    task = next((t for t in all_tasks if t[0] == input_data.task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    current_step = task[5]
    next_step = current_step + 1
    next_rev = calculate_next_revision(next_step)
    
    db.update_memory_task_step(input_data.task_id, next_rev, next_step)
    return {"status": "success", "next_step": next_step}

@app.post("/save-note")
async def save_note(input_data: ReadingNoteInput):
    db.save_reading_note(input_data.thought_id, input_data.content)
    return {"status": "success"}

@app.get("/get-notes/{thought_id}")
async def get_notes(thought_id: int):
    rows = db.get_notes_for_thought(thought_id)
    return [{"content": r[0], "date": r[1]} for r in rows]

@app.get("/memory-tasks/all")
async def get_all_tasks():
    rows = db.get_all_memory_tasks()
    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "text": r[1],
            "explanation": r[2],
            "example": r[3],
            "next_revision": r[4],
            "step": r[5],
            "created_at": r[6]
        })
    return tasks

@app.get("/morning-digest")
async def get_morning_digest():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Check if we already have it in DB
    cached = db.get_today_daybreak(today)
    history = get_history_list()
    
    if cached:
        try:
            return {"current": json.loads(cached), "history": history}
        except Exception as e:
            # If cached data is corrupted, we ignore it and generate fresh
            print(f"Error parsing cached daybreak: {e}")
    
    # 2. Generate new one if not cached or cache was invalid
    from datetime import timedelta
    thoughts = db.get_all_thoughts()[:10]
    journals = db.get_all_journal()[:10]
    history_text = "Yesterday's Insights:\n" + "\n".join([f"Thought: {r[1]}" for r in thoughts])
    history_text += "\n\nYesterday's Journal:\n" + "\n".join([f"Note: {r[0]}" for r in journals])
    
    if not history_text.strip():
        history_text = "No recorded activity yesterday. Start fresh and dominate the domain today."
        
    # Using replace instead of format for safety against user-provided brackets
    prompt = prompts.MORNING_DIGEST_PROMPT.replace("{history}", history_text).replace("{date}", today)
    digest_raw = get_ai_response(prompt)
    
    if digest_raw:
        # LLMs often wrap JSON in Markdown code blocks; let's extract it
        try:
            cleaned = digest_raw.strip()
            if cleaned.startswith("```"):
                # Handle ```json { ... } ``` or similar
                lines = cleaned.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()
            
            # Final attempt to find the first '{' and last '}' if filler text exists
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                cleaned = cleaned[start:end+1]
                
            data = json.loads(cleaned)
            # Save the clean JSON string back
            db.save_daybreak(json.dumps(data), today)
            return {"current": data, "history": history}
        except Exception as e:
            print(f"Failed to parse AI Daybreak output: {e}. Raw content: {digest_raw}")
            # If parsing fails, don't crash the server, just return no current digest
    
    return {"current": None, "history": history}

def get_history_list():
    rows = db.get_all_daybreaks()
    history = []
    for r in rows: # content_json, day_string
        try:
            history.append({"date": r[1], "content": json.loads(r[0])})
        except:
            # Skip invalid history entries instead of crashing the whole list
            pass
    return history

# --- CLOUD ROUTING FIX ---
# This ensures the main URL always points to your index.html regardless of where the server is started
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_PATH = os.path.normpath(os.path.join(BACKEND_DIR, "..", "frontend"))

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

# Serve other static files (if any)
app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "127.0.0.1" if not os.environ.get("PORT") else "0.0.0.0"
    uvicorn.run("main:app", host=host, port=port, reload=True)
