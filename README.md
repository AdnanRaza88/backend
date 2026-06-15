# GradePulse - Student Grade Tracker

Professional FastAPI backend with Streamlit dashboard for tracking student grades.

## Features
- Full CRUD operations on student grades
- Extra endpoint: Search by student name
- Groq AI powered study tips and class analysis
- Beautiful neumorphic Streamlit UI
- SQLite database
- Ready for Railway deployment

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add GROQ_API_KEY
3. `uvicorn main:app --reload`
4. In new terminal: `streamlit run streamlit_app.py`

## Deployment
- Backend: Railway (Procfile ready)
- Frontend: Streamlit Cloud or same repo