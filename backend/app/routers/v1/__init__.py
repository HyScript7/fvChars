from fastapi import APIRouter, status

from .character_controller import character_controller
from .user_controller import user_controller

v1 = APIRouter(prefix="/v1")

v1.include_router(user_controller)
v1.include_router(character_controller)


@v1.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World"}
