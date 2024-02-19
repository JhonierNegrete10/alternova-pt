from fastapi import APIRouter

from .models import CareerModel, LevelModel, SubjectModel  # noqa: F401
from .routers import career_routes, level_routes, subject_routes

api_routes = APIRouter()
api_routes.include_router(subject_routes)
api_routes.include_router(level_routes)
api_routes.include_router(career_routes)
