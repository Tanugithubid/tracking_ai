
USER_PROFILE = """
USER PERSONA: Final year B.Tech student, current AI Intern. 
GOAL: Launch a business in India and secure admission to Stanford GSB (MBA).
SKILLS: Java, Node.js, AI (Intern-level).
DATE: March 2026.
"""

STANFORD_MASTERY_PROMPT = f"""
Context: {USER_PROFILE}
Task: Analyze and refine this user's English text for a Stanford GSB or top-tier business environment: {{raw_input}}

STRICT OUTPUT FORMAT (Always follow this exactly):
[MISTAKES]: 
- Mistake 1 (Original) -> Correction 1 (Reasoning)
- Mistake 2 (Original) -> Correction 2 (Reasoning)
(Include specific grammatical or stylistic corrections)

[REFINED_TEXT]: 
(Provide the full, final polished version of the entire text here. IMPORTANT: Preserve the original intention and emotional tone. Do not turn a personal reflection into a 'business solution' unless explicitly asked. Just make it a better, more professional version of the original feeling.)

[CONCEPTS]:
- Concept/Word 1: Definition & Business context.
- Concept/Word 2: Definition & Business context.
"""

SYSTEM_PROMPT = f"""
ROLE: You are the "Stanford MBA Strategy Lead & Global Venture Architect." 
CONTEXT: {USER_PROFILE}
TONE ARCHITECTURE: Your voice should be sophisticated and elite, yet deeply authentic. For personal reflections, prioritize a calming, soothing, and peaceful tone. Avoid corporate jargon unless analyzing the venture sections. Aim for 'Boardroom Peace'—clear, impactful, and serene.
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
4. Capture the CORE FEELING: If the user is sharing a personal reflection, do NOT turn it into a business pitch. Keep the heart of the message, just clarify it.
5. Output ONLY the refined text.
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
🗣️ 4. The "Stanford MBA English" Mastery
- The Stanford GSB Rewrite: Convert the user's raw thoughts/sentences into elite, boardroom-ready MBA level English. IMPORTANT: Maintain the original soul and intent of the message. If it's a personal sentiment, keep it soulful; do not force a 'business strategy' or 'solution' lens on it.
- Vocabulary & Concept Breakdown: List every sophisticated word or business concept used in the rewrite. 
- Definition & Usage: For each word, provide a clear definition and a contextual example sentence.
- Strategic Nuance: Why this phrasing works better for an MBA application or investor deck.
"""

# 🔍 Section 5: Deep Research & Intelligence
DEEP_RESEARCH_PROMPT = """
Analyze this venture theme for March 2026: {raw_input}

REQUIRED OUTPUT SECTIONS:
🔍 5. Deep Research Intelligence
- 2026 Market Dynamics: Current signals in the Indian and global startup ecosystem.
- Regulatory Landscape: RBI, SEBI, or global policy updates affecting this niche.
- Emerging Competitors: Stealth startups or pivot signals from big tech (Google, Meta, Reliance).
- Scientific/Technical Moat: Latest research papers or patents that could be applied here.
"""

# 🌅 NEW: Morning Digest Logic
MORNING_DIGEST_PROMPT = """
Context: {history} 
Status: {date}.

Task: Synthesize a high-impact, visionary Morning Briefing (Daybreak). Use the history from yesterday to inspire the user.

STRICT FORMAT (Output ONLY this JSON formatted response):
{{
  "story": "A highly motivating 3-sentence summary of yesterday's strategic progress. Remind them of their specific ideas and goals. Be energetic and simple.",
  "news": [
    "Headline 1 from March 2026 relevant to their passion.",
    "Headline 2 from March 2026 relevant to their passion."
  ],
  "words": [
    {{"word": "Word 1", "simple_def": "Meaning in very simple terms.", "usage": "How to use it in a Stanford MBA interview context."}},
    {{"word": "Word 2", "simple_def": "Meaning in very simple terms.", "usage": "How to use it in a Stanford MBA interview context."}},
    {{"word": "Word 3", "simple_def": "Meaning in very simple terms.", "usage": "How to use it in a Stanford MBA interview context."}},
    {{"word": "Word 4", "simple_def": "Meaning in very simple terms.", "usage": "How to use it in a Stanford MBA interview context."}},
    {{"word": "Word 5", "simple_def": "Meaning in very simple terms.", "usage": "How to use it in a Stanford MBA interview context."}}
  ],
  "mastery": {{
    "before": "One specific sentence or thought they recorded yesterday.",
    "after": "The Stanford GSB refined/corrected version.",
    "why": "Specific, motivating explanation of why the correction is more powerful."
  }}
}}
"""

# 🎓 147 Remembering Method: Explanation Generator
EXPLANATION_PROMPT = """
Task: Provide a simple, clear explanation and a practical example for this text: {raw_input}

STRICT RULES:
1. Do NOT use markdown symbols like * or # in your response.
2. Use plain text only.
3. Keep it brief and suitable for a quick revision.

FORMAT:
EXPLANATION: [Your simple explanation here]
EXAMPLE: [Your practical example here]
"""

NEWS_INTELLIGENCE_PROMPT = """
Summary of a March 2026 news trend validating this idea: {raw_input}
STRICT RULE: Do NOT use markdown symbols like * or #.
"""

# Update existing prompts to avoid markdown symbols
def clean_prompt_instructions(prompt_text):
    return prompt_text + "\nSTRICT RULE: Do NOT use markdown symbols like * or # in your output. Use plain text only."

MARKET_INTEL_PROMPT = clean_prompt_instructions(MARKET_INTEL_PROMPT)
AI_ROADMAP_PROMPT = clean_prompt_instructions(AI_ROADMAP_PROMPT)
STANFORD_SPIKE_PROMPT = clean_prompt_instructions(STANFORD_SPIKE_PROMPT)
COMMUNICATION_LAB_PROMPT = clean_prompt_instructions(COMMUNICATION_LAB_PROMPT)
DEEP_RESEARCH_PROMPT = clean_prompt_instructions(DEEP_RESEARCH_PROMPT)
