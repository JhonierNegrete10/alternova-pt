from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


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
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class SubjectCreate(BaseModel):
    subject_name: str
    subject_code: str

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


LevelModel.update_forward_refs()
CareerModel.update_forward_refs()
SubjectModel.update_forward_refs()


