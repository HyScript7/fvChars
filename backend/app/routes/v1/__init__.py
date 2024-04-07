from fastapi import APIRouter

router: APIRouter = APIRouter()

from .user_router import router as user_router

router.include_router(user_router, prefix="/user")
