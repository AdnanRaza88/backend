from sqlmodel import SQLModel, Field
from typing import Optional

class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=100)
    marks_obtained: float = Field(ge=0)
    total_marks: float = Field(ge=1)
    semester: str = Field(min_length=1, max_length=20)
    date: str