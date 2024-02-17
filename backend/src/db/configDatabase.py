# SQLModel based on pydantic and SQLalchemy
import logging
from typing import Generator

from core.config import settings

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

log = logging.getLogger("uvicorn")

# DATABASE_URL=postgresql://postgres:postgres@db:5432/foo
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Return all doing in the db
    future=True,
    pool_pre_ping=True,
    # isolation_level="READ UNCOMMITTED",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    initialization of the database sync
    """
    global engine
    try:
        # db = SessionLocal()
        # SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"{__name__}: An exception occurred {e}")


def get_db() -> Generator:
    global SessionLocal
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
