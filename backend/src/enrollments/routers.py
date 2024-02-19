from typing import List

from db.configDatabase import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .crud import enrollment_crud, student_crud
from .models import EnrollmentCreate, StudentCreate, StudentModel, status

student_routes = APIRouter(prefix="/students", tags=["students"])


@student_routes.post("/")
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    """
    Create a new student in the database.
    """
    student_db: StudentModel = student_crud.create(student, session)
    return student_db


@student_routes.get("/")
def read_students(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    """
    Get a list of students from the database.
    """
    db_students = student_crud.get_all(skip, limit, session)
    return db_students


@student_routes.get("/{student_id}")
def read_student(
    student_id: int,
    session: Session = Depends(get_session),
):
    """
    Get a specific student by ID from the database.
    """
    db_student = student_crud.get_by_id(student_id, session)
    return db_student


enrollment_routes = APIRouter(prefix="/enroll", tags=["enrollments"])


@enrollment_routes.post("/")
def create_enrollment(
    enrollment: EnrollmentCreate, session: Session = Depends(get_session)
):
    """
    Create a new enrollment in the database.
    """
    db_enrollment = enrollment_crud.create(enrollment, session)
    return db_enrollment


@enrollment_routes.get("/", response_model=List[EnrollmentCreate])
def read_enrollments(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    """
    Get a list of enrollments from the database.
    """
    db_enrollments = enrollment_crud.get_all(skip, limit, session)
    return db_enrollments


@enrollment_routes.get("/students/{student_id}")
def read_subject_available_student(
    student_id: int, session: Session = Depends(get_session)
):
    """
    Get the list of available subjects for the student based on their academic progress and prerequisites.
    """
    student: StudentModel = student_crud.get_by_id(student_id, session)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_career = student.career
    if not student_career:
        raise HTTPException(status_code=404, detail="Student not have a career yet")

    subjects = student_career.subjects
    available_subjects = []
    for subject in subjects:
        prerequisite_subjects = subject.prerequisite_subjects
        if len(prerequisite_subjects) > 0:
            # Subject with prerequisite
            for prerequisite_subject in prerequisite_subjects:
                # Buscar si el estudiante ya la matriculo y aprobó
                enrollments = enrollment_crud.get_by_subject_id(
                    prerequisite_subject.id, session
                )
                for enroll in enrollments:
                    if enroll.student_id == student.id:
                        # ahora se si este enroll le pertence a este estudiante
                        if enroll.status == status.approved:
                            # tiene aprobado el prerequisito
                            available_subjects.append(
                                (
                                    subject,
                                    enroll,
                                    "prerequisite_subject_status.approved",
                                )
                            )
                        elif enroll.status == status.disapproved:
                            # Necesita volver a ver la materia perdida
                            available_subjects.append(
                                (
                                    prerequisite_subject,
                                    enroll,
                                    "prerequisite_subject_status.disapproved",
                                )
                            )

        else:  # La materia No tiene prerequisitos
            # si esa materia tiene matriculas previas relacionadas al estudiante
            enrollments = enrollment_crud.get_by_subject_id(subject.id, session)
            for enroll in enrollments:
                if enroll.student_id == student.id:
                    # ahora se si este enroll le pertence a este estudiante
                    if enroll.status == status.approved:
                        # tiene aprobado el requisito
                        pass
                    elif enroll.status == status.disapproved:
                        # Necesita volver a ver la materia perdida
                        available_subjects.append(
                            (subject, enroll, " subject_status.disapproved")
                        )
                    else:
                        # significa que todavia no ha terminado la materia
                        pass

            # la materia está disponible para matricular ya que
            # no tiene matricula previa
            # No tiene prerequisito, ni la ha perdido
            available_subjects.append((subject, "null", " subject_status.null"))
    return dict(
        available_subjects=available_subjects,
        count=len(available_subjects),
        ids=[subject.id for (subject, _, _) in available_subjects],
    )


@enrollment_routes.post("/subjects/")
def enroll_student_in_subjects(
    subject_ids: List[int], student_id: int, session: Session = Depends(get_session)
):
    """
    Enroll a student in specific subjects by providing a list of subject IDs.
    """
    enrollments = enrollment_crud.enroll_student_in_subjects(
        subject_ids, student_id, session
    )
    return enrollments


@enrollment_routes.get("/enrolled/subjects/")
def get_enrolled_subjects(student_id: int, session: Session = Depends(get_session)):
    """
    Get the list of subjects in which a student is enrolled.
    """
    subjects_enrolled = enrollment_crud.get_by_student_id(student_id, session)
    return subjects_enrolled


@enrollment_routes.put("/{enrollment_id}/finish/")
def finish_subject(
    enrollment_id: int, score: float, session: Session = Depends(get_session)
):
    """
    Finish a subject for a student by updating the score.
    """
    enrollment = enrollment_crud.get_by_id(enrollment_id, session)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment = enrollment_crud.finish_subject(enrollment, score, session)
    return enrollment


# # Endpoint para obtener la lista de materias aprobadas por un estudiante y su promedio de puntaje general
@student_routes.get("/approved/")
def get_approved_subjects(student_id: int, session: Session = Depends(get_session)):
    student: StudentModel = student_crud.get_by_id(student_id, session)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_enrollments = enrollment_crud.get_by_student_id(student_id, session)
    approved_subjects = []
    general_mean = 0
    general_count = 0
    for enroll in student_enrollments:
        if enroll.status == status.approved:
            approved_subjects.extend(
                student_crud.get_subject_filter_by_subject_id(
                    student, enroll.subject_id, session
                )
            )
        if enroll.status is None:
            continue
        general_mean += enroll.score
        general_count += 1

    return dict(
        approved_subjects=approved_subjects,
        general_mean=general_mean / general_count,
        general_count=general_count,
        approved_count=len(approved_subjects),
    )


# # Endpoint para comprobar las materias que un estudiante ha reprobado
@student_routes.get(
    "/disapproved/",
)
def get_disapproved_subjects(student_id: int, session: Session = Depends(get_session)):
    student: StudentModel = student_crud.get_by_id(student_id, session)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_enrollments = enrollment_crud.get_by_student_id(student_id, session)
    disapproved_subjects = []
    for enroll in student_enrollments:
        if enroll.status == status.disapproved:
            disapproved_subjects.extend(
                student_crud.get_subject_filter_by_enroll_subject_id(
                    student, enroll, session
                )
            )
        if enroll.status is None:
            continue

    return dict(
        disapproved_subjects=disapproved_subjects,
        disapproved_count=len(disapproved_subjects),
    )
