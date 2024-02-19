from db.configDatabase import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .crud import career_crud, level_crud, subject_crud
from .models import (
    CareerCreate,
    CareerModel,
    LevelCreate,
    LevelModel,
    SubjectCreate,
    SubjectModel,
)

subject_routes = APIRouter(prefix="/subjects", tags=["subjects"])


# Rutas
@subject_routes.post("/")  # todo: add response model
def create_subject(subject: SubjectCreate, session: Session = Depends(get_session)):
    subject_db: SubjectModel = subject_crud.create(subject, session)

    # subject_db = subject_crud.create(subject=subject, session=session)
    return subject_db


@subject_routes.get(
    "/",
    # response_model=List[SubjectResponse]
)
def read_subjects(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    db_subjects = subject_crud.get_all(skip, limit, session)
    print(db_subjects)
    return db_subjects


# Endpoint para obtener los prerequisitos de una materia
@subject_routes.get("/{subject_id}/prerequisites/")
def get_subject_prerequisites(subject_id: int, session: Session = Depends(get_session)):
    subject: SubjectModel = subject_crud.get_by_id(subject_id, session)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    prerequisites = subject.prerequisite_subjects
    return {
        "subject_name": subject.subject_name,
        "prerequisites": [prerequisite.subject_name for prerequisite in prerequisites],
    }


#! Level
level_routes = APIRouter(prefix="/levels", tags=["levels"])


@level_routes.post("/")
def create_level(level: LevelCreate, session: Session = Depends(get_session)):
    level_db: LevelModel = level_crud.create(level, session)

    return level_db


@level_routes.get("/")
def get_levels(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    level_db: LevelModel = level_crud.get_all(skip, limit, session=session)

    return level_db


#! Carrer
career_routes = APIRouter(prefix="/careers", tags=["careers"])


@career_routes.post("/")
def create_carrer(career: CareerCreate, session: Session = Depends(get_session)):
    career_db: CareerModel = career_crud.create(career, session)

    return career_db


@career_routes.get("/")
def get_carrer(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    career_db: CareerModel = career_crud.get_all(skip, limit, session=session)

    return career_db


@career_routes.get("/{career_id}/subjects")
def get_subjects_from_career(
    career_id: int,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    career_db: CareerModel = career_crud.get_subjects_from_career(
        career_id, skip, limit, session=session
    )

    return career_db.subjects


@career_routes.get("/{career_id}/students")
def get_students_from_career(
    career_id: int,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    career_db: CareerModel = career_crud.get_subjects_from_career(
        career_id, skip, limit, session=session
    )

    return career_db.students


# Endpoint to create example data
@career_routes.post("/create_example_data")
def create_example_data(session: Session = Depends(get_session)):
    # Create example levels
    level_data = [
        {"level_name": "Nivel I", "level_code": 1},
        {"level_name": "Nivel 2", "level_code": 2},
        {"level_name": "Nivel 3", "level_code": 3},
    ]
    for data in level_data:
        level = LevelCreate(**data)
        level_crud.create(level, session)

    # Create example careers
    career_data = [
        {"career_name": "Computer Science"},
        {"career_name": "Engineering"},
        {"career_name": "Business Administration"},
    ]
    for data in career_data:
        career = CareerCreate(**data)
        career_crud.create(career, session)

    # Create example subjects
    subject_data = [
        {
            "subject_name": "Introduction to Programming",
            "subject_code": "CS101",
            "level_id": 1,
            "career_id": 1,
        },
        {
            "subject_name": "Database Management",
            "subject_code": "CS201",
            "level_id": 2,
            "career_id": 1,
        },
        {
            "subject_name": "Marketing Principles",
            "subject_code": "BA101",
            "level_id": 3,
            "career_id": 1,
        },
    ]
    for data in subject_data:
        subject = SubjectCreate(**data)
        subject_crud.create(subject, session)

    for data in subject_data:
        data["career_id"] == 2
        subject = SubjectCreate(**data)
        subject_crud.create(subject, session)

    for data in subject_data:
        data["career_id"] == 3
        subject = SubjectCreate(**data)
        subject_crud.create(subject, session)
    try:
        # Create example prerequisite relationships
        prerequisite_data = [
            {"subject_id": 2, "prerequisite_id": 1},  # CS201 requires CS101
            {"subject_id": 3, "prerequisite_id": 1},  # BA101 requires CS101
        ]
        for data in prerequisite_data:
            subject_crud.create_prerequisite(data, session)
    except Exception as e:
        print("\n" * 3, f"{e}")
    return {"message": "Example data created successfully"}


# Endpoint para obtener lista de nombres de materias de una carrera
@career_routes.get("/{career_id}")
def get_career_subjects(career_id: int, session: Session = Depends(get_session)):
    career: CareerModel = career_crud.get_by_id(career_id, session)
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")

    subjects = career.subjects
    return {
        "career_name": career.career_name,
        "subjects": [subject.subject_name for subject in subjects],
    }
