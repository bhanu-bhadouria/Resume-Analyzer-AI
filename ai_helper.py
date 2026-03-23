from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rewrite_resume(resume, job_profile, missing_skills):
    if not os.getenv("OPENAI_API_KEY"):
        return "⚠️ API key not found. Please configure OPENAI_API_KEY."

    job_text = f"""
Skills: {", ".join(job_profile.get("skills", []))}
Tools: {", ".join(job_profile.get("tools", []))}
Responsibilities: {", ".join(job_profile.get("responsibilities", []))}
Keywords: {", ".join(job_profile.get("keywords", []))}
"""

    prompt = f"""
You are a top-tier ATS resume optimizer and hiring expert.

Your goal is to MAXIMIZE the resume's match score for the target role.

--- ORIGINAL RESUME ---
{resume}

--- TARGET JOB PROFILE ---
{job_text}

--- CRITICAL INSTRUCTIONS (FOLLOW STRICTLY) ---
Missing skills to add: {", ".join(missing_skills) if missing_skills else "None"}

--- STRICT INSTRUCTIONS ---

1. PRIORITY:
- Strongly align resume with job requirements
- Use same keywords as job profile

2. MISSING SKILLS HANDLING:
- Incorporate missing skills naturally where possible
- If not present, reflect them in projects or skills section

3. BULLET POINT OPTIMIZATION:
- Use: Action Verb + Tool + Task + Impact
- Add measurable outcomes (%, scale, efficiency)

4. KEYWORD DENSITY:
- Ensure high repetition of important keywords (naturally)
- ATS should easily detect relevant skills

5. STRUCTURE:
NAME
Professional Summary
Skills
Experience
Projects

6. RULES:
- No fake experience
- No fake companies
- Only enhance existing content intelligently

Return a clean, ATS-optimized resume.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a world-class resume optimizer focused on ATS scoring."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5  # Lower = more precise, less fluff
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"