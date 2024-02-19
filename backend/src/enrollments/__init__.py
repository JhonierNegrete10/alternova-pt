from .models import EnrollmentModel, StudentModel  # noqa: F401
from .routers import enrollment_routes, student_routes  # noqa: F401
from fastapi import APIRouter
api_routes = APIRouter()
api_routes.include_router(enrollment_routes)
api_routes.include_router(student_routes)