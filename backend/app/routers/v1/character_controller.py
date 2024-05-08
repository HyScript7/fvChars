from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from ...database.models import character_model, user_model
from ...schemas import generic_responses
from ...services import character_service, user_service
from ...services.errors import character_errors, user_errors

character_controller: APIRouter = APIRouter(prefix="/characters")


@character_controller.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=generic_responses.GenericMessageResponse,
)
async def root(
    current_user: user_model.User = Depends(user_service.required_get_current_user),
):
    return {"message": f"Hello {current_user}!"}
