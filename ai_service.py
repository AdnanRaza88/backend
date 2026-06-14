import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def study_tips(subject, marks_obtained, total_marks, challenges, study_hours, exam_fear):
    percentage = (marks_obtained / total_marks) * 100
    prompt = f"""
Student scored {marks_obtained}/{total_marks} ({percentage:.1f}%) in {subject}.
Challenges: {challenges}
Daily study hours: {study_hours}
Exam fear: {exam_fear}
Give 3 practical, encouraging study tips addressing these pain points. Keep concise.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

def motivation_quote(percentage):
    prompt = f"Student scored {percentage:.1f}%. Give a short, powerful motivational quote to boost confidence."
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def improvement_plan(subject, percentage):
    prompt = f"Student got {percentage:.1f}% in {subject}. Suggest a 7-day improvement plan with 3 simple daily actions."
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=250
    )
    return response.choices[0].message.content.strip()