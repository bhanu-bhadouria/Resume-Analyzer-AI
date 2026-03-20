import streamlit as st
from matcher import match_score
from utils import extract_text_from_pdf
from ai_helper import improve_resume

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:
    resume_text = extract_text_from_pdf(uploaded_file)

    score, matched, missing = match_score(resume_text, job_desc)

    #Score display
    st.subheader(f"🎯 Match Score: {score}%")

    #Columns
    col1, col2 = st.columns(2)

    with col1:
        st.write("✅ Matched Keywords")
        st.write(list(matched)[:20])

    with col2:
        st.write("❌ Missing Keywords")
        st.write(list(missing)[:20])

    #AI Suggestions Button
    st.divider()

    if st.button("💡 Get AI Suggestions"):
        with st.spinner("Analyzing with AI..."):
            suggestions = improve_resume(resume_text, job_desc)

        st.subheader("🤖 AI Suggestions")
        st.write(suggestions)