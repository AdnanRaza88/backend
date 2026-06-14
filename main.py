from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session, init_db
from models import Grade
from schemas import GradeCreate, GradeResponse
from ai_service import study_tips, motivation_quote, improvement_plan

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
    db_grade = Grade(**grade.dict())
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

@app.put("/grades/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, grade_update: GradeCreate, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in grade_update.dict().items():
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
def ai_study_tips(grade_id: int, challenges: str, study_hours: str, exam_fear: str, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    tips = study_tips(grade.subject, grade.marks_obtained, grade.total_marks, challenges, study_hours, exam_fear)
    return {"grade_id": grade_id, "study_tips": tips}

@app.post("/grades/{grade_id}/motivation")
def ai_motivation(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    percentage = (grade.marks_obtained / grade.total_marks) * 100
    quote = motivation_quote(percentage)
    return {"grade_id": grade_id, "motivation_quote": quote}

@app.post("/grades/{grade_id}/improvement-plan")
def ai_improvement_plan(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Record not found")
    percentage = (grade.marks_obtained / grade.total_marks) * 100
    plan = improvement_plan(grade.subject, percentage)
    return {"grade_id": grade_id, "improvement_plan": plan}