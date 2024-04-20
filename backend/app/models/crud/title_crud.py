from typing import List

from ... import Session
from ..title_model import TitleModel


def get_title(db: Session, id: int) -> TitleModel:
    return db.get(TitleModel, id)


def get_all_titles_by_user(db: Session, userid: int) -> List[TitleModel]:
    return db.query(TitleModel).filter_by(userid=userid).all()


def get_all_titles(db: Session) -> List[TitleModel]:
    return db.query(TitleModel).all()


def create_title(db: Session, userid: int, title: str) -> TitleModel:
    title: TitleModel = TitleModel(userid=userid, title=title)
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


def update_title(db: Session, title: TitleModel) -> TitleModel:
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


def delete_title(db: Session, title: TitleModel) -> None:
    db.delete(title)
    db.commit()
