import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GradePulse - Student Grade Tracker", layout="wide")

# Neumorphic CSS
st.markdown("""
<style>
    .stApp {
        background: #f0f2f6;
    }
    .neumorphic {
        background: #f0f2f6;
        box-shadow:  8px 8px 16px #d1d5db,
                     -8px -8px 16px #ffffff;
        border-radius: 16px;
        padding: 20px;
    }
    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 16px;
    }
    .btn-primary {
        background: linear-gradient(145deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 GradePulse")
st.markdown("**Professional Student Grade Tracker**")

BASE_URL = st.text_input("Backend API URL", value="http://localhost:8000", help="Change to deployed URL on Railway")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Dashboard", "Add Grade", "AI Tools", "Analytics"])

if page == "Dashboard":
    st.subheader("All Grades")
    try:
        resp = requests.get(f"{BASE_URL}/grades")
        if resp.status_code == 200:
            data = resp.json()
            if data:
                df = pd.DataFrame(data)
                df['percentage'] = (df['marks_obtained'] / df['total_marks'] * 100).round(2)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No grades yet. Add some!")
        else:
            st.error("Failed to fetch grades")
    except:
        st.error("Backend not reachable. Start FastAPI server.")

elif page == "Add Grade":
    st.subheader("Add New Grade")
    with st.form("add_grade"):
        student_name = st.text_input("Student Name")
        subject = st.text_input("Subject")
        marks_obtained = st.number_input("Marks Obtained", min_value=0.0)
        total_marks = st.number_input("Total Marks", min_value=1.0, value=100.0)
        semester = st.text_input("Semester", value="Spring 2026")
        date = st.date_input("Date", value=datetime.now().date())
        
        submitted = st.form_submit_button("Save Grade", type="primary")
        if submitted:
            payload = {
                "student_name": student_name,
                "subject": subject,
                "marks_obtained": marks_obtained,
                "total_marks": total_marks,
                "semester": semester,
                "date": date.strftime("%Y-%m-%d")
            }
            try:
                r = requests.post(f"{BASE_URL}/grades", json=payload)
                if r.status_code == 201:
                    st.success("Grade added successfully!")
                    st.rerun()
                else:
                    st.error(r.json().get("detail", "Error"))
            except Exception as e:
                st.error(str(e))

elif page == "AI Tools":
    st.subheader("AI Study Assistant")
    grade_id = st.number_input("Grade ID", min_value=1, step=1)
    
    if st.button("Get Personalized Study Tips", type="primary"):
        try:
            r = requests.post(f"{BASE_URL}/grades/{grade_id}/study-tips", params={
                "challenges": "Time management",
                "study_hours": "2-3 hours daily",
                "exam_fear": "Moderate"
            })
            if r.status_code == 200:
                st.markdown(f"**Tips:**\n{r.json()['study_tips']}")
            else:
                st.error("Grade not found or error")
        except:
            st.error("Connection error")

    if st.button("Overall Class Analysis"):
        try:
            r = requests.post(f"{BASE_URL}/grades/overall-analysis")
            if r.status_code == 200:
                st.markdown("**Class Analysis:**\n" + r.json().get("analysis", "No data"))
        except:
            st.error("Error")

elif page == "Analytics":
    st.subheader("Student Performance")
    try:
        resp = requests.get(f"{BASE_URL}/grades")
        if resp.status_code == 200:
            df = pd.DataFrame(resp.json())
            if not df.empty:
                df['percentage'] = (df['marks_obtained'] / df['total_marks'] * 100).round(1)
                st.bar_chart(df.set_index('student_name')['percentage'])
                st.dataframe(df[['student_name', 'subject', 'percentage', 'semester']])
    except:
        st.warning("No data or backend issue")