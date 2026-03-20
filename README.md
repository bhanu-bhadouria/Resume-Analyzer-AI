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
git clone https://github.com/bhanu-bhadouria/resume-analyzer-ai.git
cd resume-analyzer-ai

pip install -r requirements.txt
python -m spacy download en_core_web_sm

streamlit run app.py
