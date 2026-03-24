
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
    mini = get_ai_response(prompts.MINI_INSIGHT_PROMPT.format(raw_input=thought))
    if not mini: mini = f"Venture concept focusing on {thought}."
    
    full_brief = {
        "s1": get_ai_response(prompts.MARKET_INTEL_PROMPT.format(raw_input=thought)),
        "s2": get_ai_response(prompts.AI_ROADMAP_PROMPT.format(raw_input=thought)),
        "s3": get_ai_response(prompts.STANFORD_SPIKE_PROMPT.format(raw_input=thought)),
        "s4": get_ai_response(prompts.COMMUNICATION_LAB_PROMPT.format(raw_input=thought)),
        "s5": get_ai_response(prompts.NEWS_INTELLIGENCE_PROMPT.format(raw_input=thought)),
        "s6": get_ai_response(prompts.DEEP_RESEARCH_PROMPT.format(raw_input=thought))
    }
    db.save_thought(thought, mini, json.dumps(full_brief))
    return {"mini_insight": mini, "full_brief": full_brief}

@app.post("/refine-english")
async def refine_english(input_data: MasteryInput):
    text = input_data.text
    response = get_ai_response(prompts.STANFORD_MASTERY_PROMPT.format(raw_input=text))
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

@app.get("/morning-digest")
async def get_morning_digest():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if we already have it
    cached = db.get_today_daybreak(today)
    if cached:
        return {"current": json.loads(cached), "history": get_history_list()}
    
    # Generate new one
    # 1. Get yesterday's thoughts and journal
    from datetime import timedelta
    yesterday_start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    # We'll just take the last 15 entries for simplicity or everything from last 24h
    thoughts = db.get_all_thoughts()[:10]
    journals = db.get_all_journal()[:10]
    history_text = "Yesterday's Insights:\n" + "\n".join([f"Thought: {r[1]}" for r in thoughts])
    history_text += "\n\nYesterday's Journal:\n" + "\n".join([f"Note: {r[0]}" for r in journals])
    
    if not history_text.strip():
        history_text = "No recorded activity yesterday. Start fresh and dominate the domain today."
        
    digest_raw = get_ai_response(prompts.MORNING_DIGEST_PROMPT.format(history=history_text, date=today))
    
    if digest_raw:
        # Save it
        db.save_daybreak(digest_raw, today)
        return {"current": json.loads(digest_raw), "history": get_history_list()}
    
    return {"current": None, "history": get_history_list()}

def get_history_list():
    rows = db.get_all_daybreaks()
    # Format for the frontend
    history = []
    for r in rows: # content_json, day_string
        history.append({"date": r[1], "content": json.loads(r[0])})
    return history

# --- CLOUD ROUTING FIX ---
# This ensures the main URL always points to your index.html
FRONTEND_PATH = os.path.join(os.getcwd(), "..", "frontend")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

# Serve other static files (if any)
app.mount("/static", StaticFiles(directory=FRONTEND_PATH), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
