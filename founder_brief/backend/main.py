
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
        "s5": get_ai_response(prompts.NEWS_INTELLIGENCE_PROMPT.format(raw_input=thought))
    }
    db.save_thought(thought, mini, json.dumps(full_brief))
    return {"mini_insight": mini, "full_brief": full_brief}

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
    history_rows = db.get_all_thoughts()[:5]
    history_text = "\n".join([f"Thought: {r[1]}" for r in history_rows])
    digest = get_ai_response(prompts.MORNING_DIGEST_PROMPT.format(history=history_text))
    return {"content": digest or "Good morning architect!"}

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
