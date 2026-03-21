import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


# ── Prompts ───────────────────────────────────────────────────────────────────

SUMMARY_PROMPT = """
You are a professional analyst. Read the SOP document below carefully.

Your task: Write a structured summary using EXACTLY 5-6 bullet points.

Each bullet point must:
- Start with the • symbol
- Be one clear, complete sentence
- Cover a distinct aspect: purpose, scope, key steps, roles, or outcomes
- Be easy to understand by a new employee
- Be written for a {role} at {detail_level} detail level

Detail level guidance:
- Short: one simple sentence per bullet, no jargon
- Medium: one clear sentence with brief context
- Detailed: one thorough sentence with specifics and reasoning


SOP Content:
{sop_text}

Output only the bullet points. No intro sentence, no title, no extra text.
"""

TRAINING_PROMPT = """
You are an expert corporate trainer creating onboarding content for a new employee for a {role}.

Role guidance:
- Intern: Use very simple language, explain every term, be encouraging and friendly
- Employee: Use standard professional language, assume basic workplace knowledge
- Manager: Be concise, focus on oversight responsibilities, compliance, and team impact

Detail level: {detail_level}
- Short: 4-5 steps, one sentence each, no extras
- Medium: 6-8 steps, 2-3 sentences each, include Why this matters
- Detailed: 8-10 steps, full explanation each, include Why this matters AND Common mistakes to avoid

Convert the SOP below into a step-by-step training guide following the above guidance.



Rules that always apply:
- Number each step as: Step 1:, Step 2:, etc.
- Write each step in simple, plain English (no jargon)
- For Medium and Detailed: after each step add — Why this matters: [one sentence]
- For Detailed only: after Why this matters add — Mistakes to avoid: [one specific mistake]
- End with a Key Reminders section with 3 tips written for a {role}
- Add a blank line between steps for readability
- Total steps should be between 5 and 7

SOP Content:
{sop_text}
"""

QUIZ_PROMPT = """
You are a training assessment designer. Create a quiz based on the SOP below for a {role}.

Detail level: {detail_level}
- Short: 2 simple questions (1 MCQ, 1 True/False), basic recall only
- Medium: 4 questions (2 MCQ, 1 True/False, 1 Short Answer)
- Detailed: 5 questions (2 MCQ, 1 True/False, 1 Short Answer, 1 scenario-based)

Role guidance:
- Intern: Simple, straightforward questions testing basic understanding
- Employee: Standard questions testing process knowledge
- Manager: Questions focused on escalation, compliance, and decision-making

For EVERY question use this exact format:

Q[number]. [Question text]
Type: [Multiple Choice / True or False / Short Answer / Scenario]
Options: A) ... B) ... C) ... D) ...   (only for Multiple Choice)
Answer: [Correct answer]
Explanation: [One sentence explaining why]

Leave a blank line between questions.

SOP Content:
{sop_text}
"""


# ── Groq API Caller ───────────────────────────────────────────────────────────

def call_groq(prompt: str) -> str:
    """Send a prompt to Groq and return the response text."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(
            f"Groq API error: {str(e)}\n\n"
            "Check that your GROQ_API_KEY in .env is correct and valid."
        )


import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


# ── Prompts ───────────────────────────────────────────────────────────────────

SUMMARY_PROMPT = """
You are a professional business analyst. Read the SOP document below carefully.

Your task: Write a structured summary using EXACTLY 5-6 bullet points.

Each bullet point must:
- Start with the • symbol
- Be one clear, complete sentence
- Cover a distinct aspect: purpose, scope, key steps, roles, or outcomes
- Be written for a {role} at {detail_level} detail level

Detail level guidance:
- Short: one simple sentence per bullet, no jargon
- Medium: one clear sentence with brief context
- Detailed: one thorough sentence with specifics and reasoning

SOP Content:
{sop_text}

Output only the bullet points. No intro sentence, no title, no extra text.
"""

TRAINING_PROMPT = """
You are an expert corporate trainer creating onboarding content for a {role}.

Role guidance:
- Intern: Use very simple language, explain every term, be encouraging and friendly
- Employee: Use standard professional language, assume basic workplace knowledge
- Manager: Be concise, focus on oversight responsibilities, compliance, and team impact

Detail level: {detail_level}
- Short: 4-5 steps, one sentence each, no extras
- Medium: 6-8 steps, 2-3 sentences each, include Why this matters
- Detailed: 8-10 steps, full explanation each, include Why this matters AND Common mistakes to avoid

Convert the SOP below into a step-by-step training guide following the above guidance.

Rules that always apply:
- Number each step as: Step 1:, Step 2:, etc.
- For Medium and Detailed: after each step add — Why this matters: [one sentence]
- For Detailed only: after Why this matters add — Mistakes to avoid: [one specific mistake]
- End with a Key Reminders section with 3 tips written for a {role}

SOP Content:
{sop_text}
"""

QUIZ_PROMPT = """
You are a training assessment designer creating a quiz for a {role}.

Detail level: {detail_level}
- Short: 2 simple questions (1 MCQ, 1 True/False), basic recall only
- Medium: 4 questions (2 MCQ, 1 True/False, 1 Short Answer)
- Detailed: 5 questions (2 MCQ, 1 True/False, 1 Short Answer, 1 scenario-based)

Role guidance:
- Intern: Simple, straightforward questions testing basic understanding
- Employee: Standard questions testing process knowledge
- Manager: Questions focused on escalation, compliance, and decision-making

For EVERY question use this exact format:

Q[number]. [Question text]
Type: [Multiple Choice / True or False / Short Answer / Scenario]
Options: A) ... B) ... C) ... D) ...   (only for Multiple Choice)
Answer: [Correct answer]
Explanation: [One sentence explaining why]

Leave a blank line between questions.

SOP Content:
{sop_text}
"""


# ── Groq API Caller ───────────────────────────────────────────────────────────

def call_groq(prompt: str) -> str:
    """Send a prompt to Groq and return the response text."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(
            f"Groq API error: {str(e)}\n\n"
            "Check that your GROQ_API_KEY in .env is correct and valid."
        )


# ── Public Functions ──────────────────────────────────────────────────────────

def generate_summary(sop_text: str, role: str, detail_level: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        sop_text=sop_text[:5000],
        role=role,
        detail_level=detail_level
    )
    return call_groq(prompt)


def generate_training(sop_text: str, role: str, detail_level: str) -> str:
    prompt = TRAINING_PROMPT.format(
        sop_text=sop_text[:5000],
        role=role,
        detail_level=detail_level
    )
    return call_groq(prompt)


def generate_quiz(sop_text: str, role: str, detail_level: str) -> str:
    prompt = QUIZ_PROMPT.format(
        sop_text=sop_text[:5000],
        role=role,
        detail_level=detail_level
    )
    return call_groq(prompt)