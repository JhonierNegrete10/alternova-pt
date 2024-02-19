from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from ..enrollments.models import StudentModel


class LevelCreate(BaseModel):
    level_name: str
    level_code: int


class LevelModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level_name: str
    level_code: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class CareerCreate(BaseModel):
    career_name: str


class CareerModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    career_name: str
    subjects: list["SubjectModel"] = Relationship(back_populates="career")
    students: list["StudentModel"] = Relationship(back_populates="career")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class SubjectCreate(BaseModel):
    subject_name: str
    subject_code: str
    credits: int = Field(default=3)
    level_id: Optional[int]
    career_id: Optional[int]


class SubjectResponse(SubjectCreate):
    ...


class PrerequisiteSubjectLink(SQLModel, table=True):
    subject_id: Optional[int] = Field(foreign_key="subjectmodel.id", primary_key=True)
    prerequisite_id: Optional[int] = Field(
        foreign_key="subjectmodel.id", primary_key=True
    )
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class SubjectModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    subject_name: str
    subject_code: str
    credits: int
    level_id: Optional[int] = Field(default=None, foreign_key="levelmodel.id")

    prerequisite_subjects: list["SubjectModel"] = Relationship(
        link_model=PrerequisiteSubjectLink,
        sa_relationship_kwargs=dict(
            primaryjoin="SubjectModel.id == PrerequisiteSubjectLink.subject_id",
            secondaryjoin="SubjectModel.id == PrerequisiteSubjectLink.prerequisite_id",
        ),
    )

    career_id: Optional[int] = Field(default=None, foreign_key="careermodel.id")
    career: Optional[CareerModel] = Relationship(back_populates="subjects")

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


LevelModel.model_rebuild()
CareerModel.model_rebuild()
SubjectModel.model_rebuild()
