# Automated Resume Screening System (ATS)

An automated Applicant Tracking System (ATS) that evaluates resumes against job descriptions using keyword-based scoring and optional LLM-assisted recruiter insights.

## Features
- Resume vs Job Description comparison
- ATS-style keyword matching
- Skill relevance scoring
- Streamlit-based interactive UI

## Tech Stack
- Python
- Streamlit
- NLP (keyword-based analysis)
- Git & GitHub


## Project Structure

ATS_Gemini_Project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── .env                   # Environment variables (not committed)
└── venv/                  # Virtual environment (ignored)

## How to Run the Project

1. Clone the repository:
   git clone https://github.com/harinids/automated-resume-screening-system.git

2. Navigate to the project directory:
   cd automated-resume-screening-system

3. Create and activate virtual environment:
   python -m venv venv
   venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run the application:
   streamlit run app.py
## Purpose

This project demonstrates how Applicant Tracking Systems (ATS) evaluate resumes
using keyword matching, relevance scoring, and NLP-style text analysis.
It is built as a learning and portfolio project.

