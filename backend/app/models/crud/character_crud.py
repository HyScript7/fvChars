from typing import List

from ... import Session
from ..character_model import CharacterModel
from ..user_model import UserModel


def get_character(db: Session, id: int) -> CharacterModel:
    return db.get(CharacterModel, id)


def get_all_characters(db: Session, user: UserModel) -> List[CharacterModel]:
    return db.query(CharacterModel).filter_by(userid=user.id).all()


def create_character(db: Session, user: UserModel) -> CharacterModel:
    character: CharacterModel = CharacterModel(userid=user.id)
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


def update_character(db: Session, character: CharacterModel) -> CharacterModel:
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


def delete_character(db: Session, character: CharacterModel) -> None:
    db.delete(character)
    db.commit()
