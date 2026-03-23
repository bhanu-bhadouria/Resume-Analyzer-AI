
import json
import os
from openai import OpenAI

# Create client from OpenAI SDK (make sure OPENAI_API_KEY is set in env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_job_profile(job_title: str) -> dict:
    """
    Given a job title (e.g. "Data Scientist"), call the LLM to
    produce a structured job profile and return as dict with keys:
    skills, tools, responsibilities, keywords
    """
    prompt = f"""
You are an expert technical recruiter. Given the job title below, produce a concise, aggregated job profile.
Return STRICT JSON only (no extra commentary) in this exact schema:
{{
  "skills": ["skill1", "skill2", ...],
  "tools": ["tool1", "tool2", ...],
  "responsibilities": ["resp1", "resp2", ...],
  "keywords": ["kw1", "kw2", ...]
}}

Job title: "{job_title}"
Notes:
- Aggregate common requirements across many companies globally.
- Use short phrases for items.
- If unsure, return empty arrays for missing fields.
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.0
        )
        content = resp.choices[0].message.content.strip()
    except Exception as e:
        # Fail gracefully
        print("OpenAI request failed:", e)
        return {"skills": [], "tools": [], "responsibilities": [], "keywords": []}

    # Try to parse JSON from the model output. Handle simple cases where the model
    # might include backticks or stray text by searching for first { ... } block.
    try:
        # If content contains code fences, remove them
        if content.startswith("```"):
            # remove triple backticks and possible language marker
            content = "\n".join(content.split("\n")[1:-1]).strip()
        # load json
        data = json.loads(content)
        # ensure keys exist
        for k in ("skills", "tools", "responsibilities", "keywords"):
            if k not in data or not isinstance(data[k], list):
                data[k] = []
        return data
    except Exception:
        # Last resort: try to extract JSON substring
        try:
            start = content.index("{")
            end = content.rindex("}") + 1
            sub = content[start:end]
            data = json.loads(sub)
            for k in ("skills", "tools", "responsibilities", "keywords"):
                if k not in data or not isinstance(data[k], list):
                    data[k] = []
            return data
        except Exception as e:
            print("Failed to parse JSON from model output:", e)
            return {"skills": [], "tools": [], "responsibilities": [], "keywords": []}