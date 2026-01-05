import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

# Prefer Streamlit secrets (Cloud), fallback to .env (local)
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Add it to Streamlit Secrets or .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# Fast, stable model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# -----------------------------
# Helper Functions
# -----------------------------
def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    return text.strip()


def calculate_ats_score(job_description, resume_text):
    jd_words = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())

    matched = jd_words & resume_words
    missing = jd_words - resume_words

    if not jd_words:
        return 0, [], []

    score = (len(matched) / len(jd_words)) * 100
    return round(score, 2), sorted(matched), sorted(missing)


def get_gemini_response(prompt):
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 300
            }
        )
        return response.text
    except GoogleAPIError as e:
        return f"AI evaluation failed due to API issue.\n\n{str(e)}"
    except Exception as e:
        return f"AI evaluation failed.\n\n{str(e)}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="ATS Resume Analyzer",
    layout="wide"
)

st.markdown(
    """
    <h2>ATS Resume Analysis Dashboard</h2>
    <p style='color:gray'>
    Enterprise-style resume evaluation using ATS logic and AI recruiter insights
    </p>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.markdown("### Application Controls")
    st.write("Upload resume and paste job description to begin analysis.")
    st.divider()
    st.markdown("### Technologies Used")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- Gemini 2.5 Flash Lite")
    st.write("- ATS Keyword Scoring")

# Main layout
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

# -----------------------------
# Analysis Logic
# -----------------------------
if analyze:
    if not job_description or not uploaded_file:
        st.warning("Both job description and resume are required.")
        st.stop()

    with st.spinner("Extracting resume text..."):
        resume_text = extract_resume_text(uploaded_file)

    ats_score, matched, missing = calculate_ats_score(
        job_description, resume_text
    )

    st.divider()
    st.markdown("### ATS Compatibility Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Match Score", f"{ats_score}%")
    c2.metric("Matched Keywords", len(matched))
    c3.metric("Missing Keywords", len(missing))

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Matched Skills")
        if matched:
            st.success(", ".join(matched[:60]))
        else:
            st.info("No strong keyword matches found.")

    with c2:
        st.markdown("### Missing Skills")
        if missing:
            st.error(", ".join(missing[:60]))
        else:
            st.success("No major gaps detected.")

    st.divider()
    st.markdown("### AI Recruiter Evaluation")

    ai_prompt = f"""
You are a senior technical recruiter evaluating a candidate for a 2–3 month internship.

Job Description:
{job_description}

Resume:
{resume_text}

Provide:
1. Overall suitability for the role
2. Key strengths relevant to the job
3. Major skill gaps or weaknesses
4. Clear, actionable improvement suggestions

Keep the response concise and practical.
"""

    with st.spinner("Generating recruiter insights..."):
        ai_response = get_gemini_response(ai_prompt)

    st.write(ai_response)
    st.success("ATS analysis completed successfully.")
