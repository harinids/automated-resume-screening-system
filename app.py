import os
from dotenv import load_dotenv

import streamlit as st
from PyPDF2 import PdfReader
from google import genai


"""
Enterprise ATS Resume Analyzer
Evaluates resume compatibility against job descriptions
using ATS-style keyword matching and Gemini AI insights.
"""


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY is missing. Please check your environment variables.")
    st.stop()

client = genai.Client(api_key=API_KEY)


def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def calculate_ats_score(job_description, resume_text):
    jd_words = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())

    matched = jd_words.intersection(resume_words)
    missing = jd_words.difference(resume_words)

    if not jd_words:
        return 0, [], []

    score = (len(matched) / len(jd_words)) * 100
    return round(score, 2), sorted(matched), sorted(missing)


def get_gemini_response(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return response.text


st.set_page_config(
    page_title="Enterprise ATS Analyzer",
    layout="wide"
)

st.markdown(
    "<h2 style='margin-bottom:0'>ATS Resume Analysis Dashboard</h2>"
    "<p style='color:gray'>Enterprise-style resume evaluation using ATS logic and AI</p>",
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown("### Application Controls")
    st.write("Upload resume and paste job description to begin analysis.")
    st.divider()
    st.write("Technologies Used")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- Gemini AI")
    st.write("- ATS Keyword Scoring")


left, right = st.columns(2)

with left:
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the complete job description here",
        height=300
    )

with right:
    uploaded_file = st.file_uploader(
        "Resume Upload (PDF)",
        type=["pdf"]
    )

analyze = st.button("Run ATS Analysis", use_container_width=True)


if analyze:
    if not job_description or not uploaded_file:
        st.warning("Both job description and resume are required.")
        st.stop()

    with st.spinner("Processing resume..."):
        resume_text = extract_resume_text(uploaded_file)

    ats_score, matched, missing = calculate_ats_score(
        job_description,
        resume_text
    )

    st.divider()

    st.markdown("### ATS Compatibility Overview")

    m1, m2, m3 = st.columns(3)
    m1.metric("ATS Match Score", f"{ats_score}%")
    m2.metric("Matched Keywords", len(matched))
    m3.metric("Missing Keywords", len(missing))

    st.divider()

    k1, k2 = st.columns(2)

    with k1:
        st.markdown("### Matched Skills & Keywords")
        if matched:
            st.success(", ".join(matched[:60]))
        else:
            st.info("No strong keyword matches detected.")

    with k2:
        st.markdown("### Missing or Weak Skills")
        if missing:
            st.error(", ".join(missing[:60]))
        else:
            st.success("No major missing skills detected.")

    st.divider()

    st.markdown("### AI Recruiter Evaluation")

    ai_prompt = f"""
    You are a senior technical recruiter reviewing a candidate profile.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Provide:
    - Suitability summary
    - Strengths and weaknesses
    - Skill gaps impacting ATS score
    - Clear improvement recommendations
    """

    with st.spinner("Generating recruiter insights..."):
        ai_response = get_gemini_response(ai_prompt)

    st.write(ai_response)

    st.success("ATS analysis completed successfully.")
