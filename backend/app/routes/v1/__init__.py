from fastapi import APIRouter

api: APIRouter = APIRouter()

from .user_router import router as user_router

api.include_router(user_router, prefix="/user")
