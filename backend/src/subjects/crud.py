from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from .models import (
    CareerModel,
    LevelModel,
    PrerequisiteSubjectLink,
    SubjectModel,
)


class BaseCRUD:
    def __init__(self):
        self.model: SQLModel

    def create(self, obj: SQLModel, session: Session):
        db_obj = self.model(**obj.dict())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_all(self, skip, limit, session: Session):
        statement = select(self.model).offset(skip).limit(limit)
        result = session.execute(statement)
        result = result.scalars().all()
        return [obj_db for obj_db in result]

    def get_by_id(self, id, session: Session):
        statement = select(self.model).where(self.model.id == id)
        result = session.execute(statement)
        obj = result.scalars().first()
        return obj


class SubjectCRUD(BaseCRUD):
    model = SubjectModel

    def create_prerequisite(self, prerequisite_subject, session: Session):
        prerequisite_link = PrerequisiteSubjectLink(**prerequisite_subject)
        session.add(prerequisite_link)
        session.commit()
        session.refresh(prerequisite_link)
        return prerequisite_link


class LevelCRUD(BaseCRUD):
    model = LevelModel


class CareerCRUD(BaseCRUD):
    model = CareerModel

    def get_subjects_from_career(self, id, skip, limit, session: Session):
        statement = (
            select(CareerModel).offset(skip).limit(limit).where(CareerModel.id == id)
        )
        result = session.execute(statement)
        result = result.scalars().first()
        return result


subject_crud = SubjectCRUD()
level_crud = LevelCRUD()
career_crud = CareerCRUD()
