from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def improve_resume(resume, jd):
    if not os.getenv("OPENAI_API_KEY"):
        return "⚠️ API key not found. Please configure OPENAI_API_KEY."

    prompt = f"""
You are an expert ATS resume optimizer.

Analyze the resume against the job description.

Resume:
{resume}

Job Description:
{jd}

Provide:
1. Missing important keywords
2. 3 improved resume bullet points
3. Suggestions to improve ATS score
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"