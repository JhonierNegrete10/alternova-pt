from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlmodel import Session, select

if TYPE_CHECKING:
    from ..subjects.models import CareerModel, SubjectModel
from .models import (
    EnrollmentCreate,
    EnrollmentModel,
    StudentCreate,
    StudentModel,
    status,
)


class EnrollmentCRUD:
    def create(self, enrollment: EnrollmentCreate, session: Session) -> EnrollmentModel:
        db_obj = EnrollmentModel(**enrollment.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_all(self, skip: int, limit: int, session: Session) -> list[EnrollmentModel]:
        statement = select(EnrollmentModel).offset(skip).limit(limit)
        result = session.exec(statement)
        return result.all()

    def get_by_id(self, id: int, session: Session) -> EnrollmentModel:
        statement = select(EnrollmentModel).where(EnrollmentModel.id == id)
        result = session.exec(statement)
        return result.first()

    def get_by_student_id(
        self, student_id: int, session: Session
    ) -> list[EnrollmentModel]:
        statement = select(EnrollmentModel).where(
            EnrollmentModel.student_id == student_id
        )
        result = session.exec(statement)
        return result.all()

    def get_by_subject_id(
        self, subject_id: int, session: Session
    ) -> list[EnrollmentModel]:
        statement = select(EnrollmentModel).where(
            EnrollmentModel.subject_id == subject_id
        )
        result = session.exec(statement)
        return result.all()

    def update_score(
        self, enrollment: EnrollmentModel, score: int, session: Session
    ) -> EnrollmentModel:
        enrollment.score = score
        enrollment.status = status.approved if score >= 3.0 else status.disapproved
        enrollment.updated_at = datetime.now()
        session.commit()
        session.refresh(enrollment)
        return enrollment

    def enroll_student_in_subjects(
        self, subject_ids: List[int], student_id: int, session: Session
    ) -> List[EnrollmentModel]:
        enrollments = []
        for subject_id in subject_ids:
            try:
                enrollment = EnrollmentModel(
                    student_id=student_id, subject_id=subject_id
                )
                session.add(enrollment)
                enrollments.append(enrollment)
            except Exception as e:
                print(f"An exception occurred {e}")
                print(f"{subject_id}")
        session.commit()
        return enrollments

    def finish_subject(
        self, enrollment, score: float, session: Session
    ) -> EnrollmentModel:
        enrollment = self.update_score(enrollment, score, session)
        return enrollment


enrollment_crud = EnrollmentCRUD()


class StudentCRUD:
    def create(self, student: StudentCreate, session: Session) -> StudentModel:
        db_obj = StudentModel(**student.model_dump())
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_all(self, skip: int, limit: int, session: Session) -> list[StudentModel]:
        statement = select(StudentModel).offset(skip).limit(limit)
        result = session.exec(statement)
        return result.all()

    def get_by_id(self, id: int, session: Session) -> StudentModel:
        statement = select(StudentModel).where(StudentModel.id == id)
        result = session.exec(statement)
        return result.first()

    def get_student_career(self, id: int, session: Session) -> list[tuple]:
        student = self.get_by_id(id, session)
        career: CareerModel = student.career
        return career

    def subjects_without_prerequisites(self, id: int, session: Session) -> list[tuple]:
        student = self.get_by_id(id, session)
        career: CareerModel = student.career
        result: list[SubjectModel] = career.subjects
        return [
            (
                obj_db.id,
                obj_db.subject_name,
                obj_db.subject_code,
                obj_db.prerequisite_subjects,
            )
            for obj_db in result
        ]

    def get_subject_filter_by_enroll_subject_id(
        self, student: StudentModel, enroll: EnrollmentModel, session: Session
    ):
        return [
            dict(subject=subject.model_dump(), enroll=enroll.model_dump())
            for subject in student.subjects
            if subject.id == enroll.subject_id
        ]


student_crud = StudentCRUD()
