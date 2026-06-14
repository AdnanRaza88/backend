from pydantic import BaseModel, Field, validator
from datetime import datetime

class GradeCreate(BaseModel):
    student_name: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=100)
    marks_obtained: float = Field(ge=0)
    total_marks: float = Field(ge=1)
    semester: str = Field(min_length=1, max_length=20)
    date: str

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be YYYY-MM-DD')
        return v

    @validator('marks_obtained')
    def marks_not_exceed_total(cls, v, values):
        if 'total_marks' in values and v > values['total_marks']:
            raise ValueError('Marks obtained cannot exceed total marks')
        return v

class GradeResponse(BaseModel):
    id: int
    student_name: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: str
    date: str