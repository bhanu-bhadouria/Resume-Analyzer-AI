# AI Resume Analyzer

An AI-powered ATS (Applicant Tracking System) Resume Analyzer that evaluates how well a resume matches a job description using NLP and semantic similarity.

---

## Features

- ✅ Keyword-based matching using NLP (spaCy)
- ✅ Lemmatization & phrase detection
- ✅ Noise filtering (removes irrelevant words)
- ✅ Synonym-aware normalization
- ✅ Skill-based weighted scoring
- ✅ Embedding-based semantic similarity
- ✅ Missing keyword detection
- ✅ AI-powered resume suggestions (OpenAI)

---

## Tech Stack

- Python
- Streamlit
- spaCy
- Sentence Transformers
- Scikit-learn
- OpenAI API

---

## How it Works

1. Extracts text from resume (PDF)
2. Cleans and normalizes text
3. Extracts keywords using NLP
4. Computes:
   - Keyword match score
   - Skill match score
   - Semantic similarity (embeddings)
5. Generates:
   - Match score
   - Missing keywords
   - AI suggestions

---

## Installation

```bash
git clone https://github.com/bhanu-bhadouria/Resume-Analyzer-AI.git
cd resume-analyzer-ai

pip install -r requirements.txt
python -m spacy download en_core_web_sm

streamlit run app.py

<img width="1920" height="857" alt="Screenshot 2026-03-21 at 1 45 40 PM" src="https://github.com/user-attachments/assets/9b42dc48-30c6-4015-8af1-74ff56c1af42" />

<img width="1920" height="708" alt="Screenshot 2026-03-21 at 1 56 48 PM" src="https://github.com/user-attachments/assets/433c4159-a24e-43ad-99c6-3c6a62c07db8" />

<img width="1920" height="858" alt="Screenshot 2026-03-21 at 1 57 07 PM" src="https://github.com/user-attachments/assets/7eec3a13-7a98-4a43-a5b8-dac6cdaa82c5" />
