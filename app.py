import streamlit as st
from job_profile_matching import generate_job_profile
from matcher import match_score
from utils import extract_text_from_pdf
from ai_helper import rewrite_resume
from pdf_generator import generate_pdf

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    st.markdown("### About")
    st.write(
        "This AI tool analyzes your resume against real-world job expectations "
        "and provides actionable improvement suggestions."
    )

    st.markdown("### Tips")
    st.write(
        "- Use a detailed resume\n"
        "- Try different job roles\n"
        "- Focus on missing skills"
    )

# Main Title
st.title("📄 AI Resume Analyzer")
st.markdown("### 🎯 Analyze your resume against real-world job expectations")
st.divider()

# Input Section
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])

with col2:
    job_title = st.text_input("💼 Enter Target Job Role")

# Generate Job Profile
job_profile = None
if job_title:
    with st.spinner("🧠 Analyzing global job market..."):
        job_profile = generate_job_profile(job_title)

    st.subheader("🧠 Market Job Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📌 Skills")
        st.write(job_profile.get("skills", []))

        st.markdown("#### 🛠 Tools")
        st.write(job_profile.get("tools", []))

    with col2:
        st.markdown("#### 📋 Responsibilities")
        st.write(job_profile.get("responsibilities", []))

        st.markdown("#### 🔑 Keywords")
        st.write(job_profile.get("keywords", []))

    st.divider()

# Main Analysis
if uploaded_file and job_profile:
    with st.spinner("🔍 Analyzing resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

        score, matched, missing = match_score(resume_text, job_profile)
        missing_skills = list(missing)

    # Score Section
    st.subheader("📊 Resume Match Analysis")

    col1, col2, col3 = st.columns(3)

    with col2:
        st.metric(label="Match Score", value=f"{score}%")

    # Matched vs Missing
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Strengths")
        if matched:
            st.success(", ".join(list(matched)[:10]))
        else:
            st.write("No strong matches found")

    with col2:
        st.markdown("### ❌ Areas to Improve")
        if missing:
            st.error(", ".join(list(missing)[:10]))
        else:
            st.write("No major gaps detected")

    # AI Suggestions
    st.divider()
    st.subheader("🧾 AI Resume Rewrite")

    if st.button("🚀 Generate Optimized Resume"):
        with st.spinner("Rewriting your resume..."):
            new_resume = rewrite_resume(resume_text, job_profile, missing_skills)

            st.success("Your optimized resume is ready 👇")

            st.markdown(new_resume)

            # Generate PDF
            pdf_file = generate_pdf(new_resume)

            if pdf_file:
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                label="📥 Download as PDF",
                data=pdf_bytes,
                file_name="optimized_resume.pdf",
                mime="application/pdf"
                )
            else:
                st.error("❌ Failed to generate PDF")