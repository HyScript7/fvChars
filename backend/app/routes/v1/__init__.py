from fastapi import APIRouter

router: APIRouter = APIRouter()

from .user_router import router as user_router
from .character_router import router as character_router

router.include_router(user_router, prefix="/user")
router.include_router(character_router, prefix="/character")
