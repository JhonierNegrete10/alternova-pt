from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.subjects.models import CareerModel, SubjectModel


class status(Enum):
    approved: str = "Approved"
    disapproved: str = "Disapproved"


class EnrollmentCreate(BaseModel):
    student_id: int
    subject_id: int
    score: Optional[float]


class EnrollmentModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_id: Optional[int] = Field(foreign_key="studentmodel.id")
    subject_id: Optional[int] = Field(foreign_key="subjectmodel.id")
    score: Optional[float]
    status: Optional[status]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class StudentCreate(BaseModel):
    # id: int
    student_name: str
    career_id: Optional[int]


class StudentModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    career_id: Optional[int] = Field(default=None, foreign_key="careermodel.id")
    career: Optional["CareerModel"] = Relationship(back_populates="students")
    subjects: list["SubjectModel"] = Relationship(link_model=EnrollmentModel)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
