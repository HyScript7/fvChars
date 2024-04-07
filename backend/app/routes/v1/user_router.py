from fastapi import Depends, APIRouter, HTTPException

from ...database import get_db, Session
from ...models import UserModel
from ...schemas import user_schema, default_schema
from ...services import user_service
from ...errors.user_errors import (
    EmailAlreadyTakenException,
    UsernameAlreadyTakenException,
    UserNotFound,
    InvalidLogin,
)

router: APIRouter = APIRouter()


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
