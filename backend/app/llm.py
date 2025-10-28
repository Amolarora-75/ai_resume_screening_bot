
import os
from typing import Dict, Any

def llm_review(text:str, job_description:str|None=None) -> Dict[str, Any]:
    """Use Gemini via LangChain if key exists; otherwise return heuristic suggestions."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        # Fallback
        suggestions = []
        if "project" not in text.lower():
            suggestions.append("Add a Projects section with 2–3 quantified bullet points.")
        if "github" not in text.lower():
            suggestions.append("Add a GitHub link showcasing your work.")
        if job_description:
            suggestions.append("Tailor your summary to mention 2–3 keywords from the job description.")
        return {
            "resume_rating": 7,
            "improvement_areas": "• Tighten bullets; use action verbs and impact numbers.\n• Keep to 1-2 pages; prioritize recent work.",
            "upskill_suggestions": "\n".join(suggestions) or "Deepen relevant frameworks and tooling."
        }

    # Real Gemini path
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.schema import HumanMessage
        chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.2)
        prompt = f"""Act as a senior technical recruiter.
Given this resume text (triple backticks) and job description (if any), return a concise JSON with:
- resume_rating (1-10)
- improvement_areas (string with bullet-like lines)
- upskill_suggestions (string with bullet-like lines)

Resume:
```{text[:12000]}```

Job description (optional):
```{job_description or ""}```

Respond with ONLY valid JSON with keys: resume_rating, improvement_areas, upskill_suggestions.
"""
        resp = chat([HumanMessage(content=prompt)])
        import json
        data = json.loads(resp.content)
        return data
    except Exception as e:
        return {
            "resume_rating": 7,
            "improvement_areas": "LLM call failed; fallback suggestions. Ensure consistent formatting and quantified impact.",
            "upskill_suggestions": "Consider practicing DSA + system design basics and strengthen key frameworks mentioned in the JD."
        }
