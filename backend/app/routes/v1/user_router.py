from fastapi import APIRouter, Depends, HTTPException

from ...database import Session, get_db
from ...errors.user_errors import (
    EmailAlreadyTakenException,
    InvalidLogin,
    UsernameAlreadyTakenException,
    UserNotFound,
)
from ...middleware.sessions import get_user_session, UserSession
from ...models import UserModel
from ...schemas import default_schema, user_schema
from ...services import user_service

router: APIRouter = APIRouter()


@router.get(
    "/me",
    response_model=user_schema.UserResponse,
    responses={401: {"model": default_schema.GenericHTTPException}},
)
async def whoami(
    db: Session = Depends(get_db), session: UserSession = Depends(get_user_session)
):
    return session.user


@router.post(
    "/register",
    response_model=user_schema.UserResponse,
    responses={409: {"model": default_schema.GenericHTTPException}},
)
async def register(body: user_schema.UserSignup, db: Session = Depends(get_db)):
    user: UserModel | None = None
    try:
        user = user_service.register_user(db, body.username, body.password, body.email)
    except EmailAlreadyTakenException:
        raise HTTPException(status_code=409, detail="Email already taken")
    except UsernameAlreadyTakenException:
        raise HTTPException(status_code=409, detail="Username already taken")
    return user


@router.post(
    "/login",
    response_model=user_schema.UserSession,
    responses={
        401: {"model": default_schema.GenericHTTPException},
        404: {"model": default_schema.GenericHTTPException},
    },
)
async def login(body: user_schema.UserSignin, db: Session = Depends(get_db)):
    user: UserModel | None = None
    try:
        user = user_service.login_user(db, body.username, body.password)
    except InvalidLogin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    token: str = user_service.create_token(user)
    return user_schema.UserSession(
        username=user.username, id=user.id, email=user.email, token=token
    )
