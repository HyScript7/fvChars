from typing import List

from ..database import CharacterModel, Session, UserModel
from ..models.crud import character_crud


def create_character(db: Session, user: UserModel) -> CharacterModel:
    character = character_crud.create_character(db, user.id)
    return character


def delete_character(db: Session, char: CharacterModel) -> None:
    character_crud.delete_character(db, char)


def get_characters(db: Session, user: UserModel) -> List[CharacterModel]:
    return character_crud.get_all_characters(db, user.id)


def get_character(db: Session, id: int) -> CharacterModel:
    return character_crud.get_character(db, id)
