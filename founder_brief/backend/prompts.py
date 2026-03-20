
USER_PROFILE = """
USER PERSONA: Final year B.Tech student, current AI Intern. 
GOAL: Launch a business in India and secure admission to Stanford GSB (MBA).
SKILLS: Java, Node.js, AI (Intern-level).
DATE: March 2026.
"""

SYSTEM_PROMPT = f"""
ROLE: You are the "Stanford MBA Strategy Lead & Global Venture Architect." 
CONTEXT: {USER_PROFILE}
"""

# 💎 Section 1: Market Intel
MARKET_INTEL_PROMPT = """
Analyze this business idea for the 2026 Indian ecosystem: {raw_input}

REQUIRED OUTPUT SECTIONS:
💎 1. The Vision & Market Intel
- Concept: A refined, high-level summary.
- The Indian Scenario: How this solves a problem in 2026 India (DPI, UPI, ONDC integration).
- Global Benchmark: Competition (Etsy, OpenAI, Google).
- Moat: Defensibility & P&L Drivers.
- Business Scenario: Step-by-step User Journey & Revenue Simulation.
"""

# ✨ NEW: The "Mini-Insight" for the main gallery
MINI_INSIGHT_PROMPT = """
Take this raw vision: {raw_input}
Rewrite it into a single, high-impact "Executive Spark" (1-2 sentences). 
STRICT RULES:
1. No "academic" or "tough" words (Avoid: burgeoning, leveraging, artisan, burgeoning).
2. Use **SIMPLE, POWERFUL** English (Use: grow, start, build, sell).
3. Start directly with the vision.
4. Output ONLY the refined text.
"""

# 🛠️ Section 2: Technical
AI_ROADMAP_PROMPT = """
Business Idea: {raw_input}
User Profile: CS student, Java/Node.js, AI Intern.

REQUIRED OUTPUT SECTIONS:
🛠️ 2. Technical & Implementation Roadmap
- The AI Layer: Architect Agentic Workflows or Vertical AI engines for this.
- Skill Gap: Advanced AI skills needed beyond Java/Node.js.
"""

# 🌲 Section 3: Stanford Spike
STANFORD_SPIKE_PROMPT = """
Business Idea: {raw_input}

REQUIRED OUTPUT SECTIONS:
🌲 3. The "Stanford Spike" Strategy
- Intellectual Vitality: How this shows deep thinking.
- Leadership Narrative: Social impact or team leadership for GSB essay "What matters most".
"""

# 🗣️ Section 4: Communication & English Mastery
COMMUNICATION_LAB_PROMPT = """
Raw Thought: {raw_input}

REQUIRED OUTPUT SECTIONS:
🗣️ 4. The "MBA Communication" Lab
- The Executive Rewrite: A 3-4 sentence professional pitch.
- Power Vocabulary: 5 MBA-level words/idioms.
- Practice Session: One specific "Sentence Starter" for today.
"""

# 🌅 NEW: Morning Digest Logic
MORNING_DIGEST_PROMPT = """
Context: {history}
User: AI Intern, Stanford MBA Aspirant.
Status: March 21, 2026. 7:00 AM.

STRICT FORMAT (Output ONLY this):
[STORY]: One short, energetic morning message to wake up the founder. (3 sentences max).
[NEWS]: List 2 headlines from March 2026 relevant to their passion.
[WORDS]: 5 MBA-level words + 1-sentence easy definition.
[MASTERY]: 
Before: (One sentence they wrote yesterday)
After: (The Stanford GSB boardroom version of that sentence)
Why: (1 sentence on the improvement)
"""

NEWS_INTELLIGENCE_PROMPT = """
Summary of a March 2026 news trend validating this idea: {raw_input}
"""
