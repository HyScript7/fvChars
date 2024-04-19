from fastapi import APIRouter, Depends, HTTPException, status

from ...database import Session, get_db
from ...middleware.sessions import UserSession, get_user_session
from ...models import CharacterModel
from ...schemas import character_schema, default_schema
from ...services import character_service

router: APIRouter = APIRouter()


@router.post(
    "/create",
    response_model=character_schema.CharacterResponse,
    responses={401: {"model": default_schema.GenericHTTPException}},
)
async def whoami(
    db: Session = Depends(get_db), session: UserSession = Depends(get_user_session)
):
    if session.is_guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must provide a token to create characters!",
        )
    character = character_service.create_character(db, session.user)
    return character
