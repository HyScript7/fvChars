from fastapi import Depends, HTTPException

from ..database import Session, get_db
from ..models import UserModel
from ..schemas import user_schema
from ..services import user_service


class UserSession:
    _user: UserModel | None

    def __init__(self, db: Session, token: str | None):
        if token:
            self._user = user_service.session_user(db, token)
        else:
            self._user = None

    def refresh(self, db: Session):
        if self._user is not None:
            db.refresh(self._user)

    @property
    def user(self) -> UserModel | None:
        if self._user is not None:
            return self._user
        else:
            user = UserModel(email="guest", username="guest", password="guest")
            user.id = 0
            return user

    @property
    def is_logged_in(self) -> bool:
        return self._user is not None

    @property
    def is_guest(self) -> bool:
        return self._user is None


async def get_user_session(
    db: Session = Depends(get_db),
    token: user_schema.UserToken = Depends(user_schema.UserToken),
) -> UserSession:
    return UserSession(db, token.token)
