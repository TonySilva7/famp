from fastapi import APIRouter
from api.v1.endpoints import course


api_router = APIRouter()

# este prefix ('/course') será concatenado com o prefix da linha 13 de configs.py ('/api/v1')
api_router.include_router(course.router, prefix="/courses", tags=["courses"])
