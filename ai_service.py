from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI service error: {str(e)}"

def study_tips(subject: str, marks_obtained: float, total_marks: float, challenges: str, study_hours: str, exam_fear: str) -> str:
    percentage = (marks_obtained / total_marks) * 100
    prompt = f"""You are an experienced teacher. Student scored {percentage:.1f}% in {subject}.
Challenges: {challenges}
Study hours: {study_hours}
Exam fear: {exam_fear}

Give 4-5 personalized study tips and a motivational message."""
    return get_ai_response(prompt)

def overall_analysis(grades) -> str:
    prompt = f"""Analyze this class performance data: {grades}
Provide overall class insights, weak subjects, top performers suggestions."""
    return get_ai_response(prompt)