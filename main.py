from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session, init_db
from models import Grade
from schemas import GradeCreate, GradeResponse
from ai_service import study_tips, overall_analysis
import os

app = FastAPI(title="Student Grade Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/grades", response_model=GradeResponse, status_code=201)
def create_grade(grade: GradeCreate, session: Session = Depends(get_session)):
    db_grade = Grade(**grade.model_dump())
    session.add(db_grade)
    session.commit()
    session.refresh(db_grade)
    return db_grade

@app.get("/grades", response_model=list[GradeResponse])
def read_grades(session: Session = Depends(get_session)):
    return session.exec(select(Grade)).all()

@app.get("/grades/{grade_id}", response_model=GradeResponse)
def read_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    return grade

@app.get("/grades/student/{student_name}")
def read_student_grades(student_name: str, session: Session = Depends(get_session)):
    grades = session.exec(select(Grade).where(Grade.student_name == student_name)).all()
    return grades

@app.put("/grades/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, grade_update: GradeCreate, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in grade_update.model_dump().items():
        if value is not None:
            setattr(grade, key, value)
    session.commit()
    session.refresh(grade)
    return grade

@app.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    session.delete(grade)
    session.commit()
    return {"ok": True}

@app.post("/grades/{grade_id}/study-tips")
def get_study_tips(grade_id: int, challenges: str = "None", study_hours: str = "None", exam_fear: str = "None", session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    tips = study_tips(grade.subject, grade.marks_obtained, grade.total_marks, challenges, study_hours, exam_fear)
    return {"grade_id": grade_id, "study_tips": tips}

@app.post("/grades/overall-analysis")
def get_overall_analysis(session: Session = Depends(get_session)):
    grades = session.exec(select(Grade)).all()
    if not grades:
        return {"message": "No grades available"}
    analysis = overall_analysis([{"student": g.student_name, "subject": g.subject, "percentage": (g.marks_obtained / g.total_marks)*100} for g in grades])
    return {"analysis": analysis}