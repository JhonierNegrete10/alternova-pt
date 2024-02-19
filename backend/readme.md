# Solución Prueba técnica 

from sqlmodel import SQLModel, Field, ForeignKey

class Student(SQLModel, table=True):
    student_id: int = Field(primary_key=True)
    name: str
    last_name: str
    email: str
    date_of_birth: str

class Subject(SQLModel, table=True):
    subject_id: int = Field(primary_key=True)
    name: str
    credits: int
    min_passing_grade: float

class Enrollment(SQLModel, table=True):
    enrollment_id: int = Field(primary_key=True)
    student_id: ForeignKey = Field(foreign_key="student.student_id")
    subject_id: ForeignKey = Field(foreign_key="subject.subject_id")
    score: float
