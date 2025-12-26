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

## Project Structure

The project is intentionally kept simple and easy to understand.

- `app.py`  
  Contains the complete Streamlit application including resume upload, ATS scoring logic, and AI-based feedback.

- `requirements.txt`  
  Lists all Python dependencies required to run the application.

- `README.md`  
  Documentation explaining the purpose, setup steps, and usage of the project.

- `.gitignore`  
  Ensures virtual environments and sensitive files are not committed to GitHub.

- `.env`  
  Stores the Gemini API key locally (not pushed to GitHub).

- `venv/`  
  Local Python virtual environment used during development.



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

## Development Notes

This project was built incrementally by experimenting with keyword matching logic and gradually enhancing it using AI-based insights.  
The focus was on understanding how real Applicant Tracking Systems filter resumes rather than building a production-ready product.

The application was tested locally using Streamlit before being pushed to GitHub.

