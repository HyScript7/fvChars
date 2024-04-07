import secrets
from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import jwt, JWTError

from ..database import Session, UserModel
from ..models.crud import user_crud
from ..errors.user_errors import (
    UsernameAlreadyTakenException,
    EmailAlreadyTakenException,
    InvalidLogin,
    UserNotFound,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_secret: str = secrets.token_hex(32)

expires_in: timedelta = timedelta(days=1)


def register_user(db: Session, username: str, password: str, email: str) -> UserModel:
    hashed_password = pwd_context.hash(password)
    if user_crud.get_user_by_email(db, email) is not None:
        raise EmailAlreadyTakenException(email)
    if user_crud.get_user_by_username(db, username) is not None:
        raise UsernameAlreadyTakenException(username)
    user = user_crud.create_user(db, username, hashed_password, email)
    return user


def login_user(db: Session, username: str, password: str) -> UserModel:
    user = user_crud.get_user_by_username(db, username)
    if user is None:
        raise UserNotFound(username)
    if not pwd_context.verify(password, user.password):
        raise InvalidLogin()
    return user


def create_token(user: UserModel) -> str:
    expire: datetime = datetime.now() + expires_in
    payload = {"id": user.id, "exp": expire}
    return jwt.encode(payload, jwt_secret, algorithm="HS256")


def validate_token(db: Session, token: str) -> UserModel:
    try:
        data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return user_crud.get_user(db, id=data.get("id"))
    except JWTError:
        raise InvalidLogin()


def session_user(db: Session, token: str) -> UserModel | None:
    try:
        return validate_token(db, token)
    except InvalidLogin:
        return None
