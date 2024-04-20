from typing import List

from sqlalchemy.exc import IntegrityError

from ..database import Session, TitleModel, UserModel
from ..errors.title_errors import DuplicateTitleValueException
from ..models.crud import title_crud


def create_title(db: Session, user: UserModel, body: str) -> TitleModel:
    try:
        title = title_crud.create_title(db, user.id, body)
        return title
    except IntegrityError:
        raise DuplicateTitleValueException(body)


def delete_title(db: Session, title: TitleModel) -> None:
    title_crud.delete_title(db, title)


def get_titles(db: Session, user: UserModel) -> List[TitleModel]:
    return title_crud.get_all_titles_by_user(db, user.id)


def get_all_titles(db: Session) -> List[TitleModel]:
    return title_crud.get_all_titles(db)


def get_title(db: Session, id: int) -> TitleModel:
    return title_crud.get_title(db, id)
