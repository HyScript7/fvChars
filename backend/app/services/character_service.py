from typing import List

from ..database.models import user_model
from ..database.models.character_model import Character, CharacterCreate

# from .errors.character_errors import (...)


async def create_character(
    user: user_model.User, character_create: CharacterCreate
) -> Character:
    """
    Create a new character in the database.

    Args:
        character_create (CharacterCreate): The character data to create.

    Returns:
        Character: The created character.
    """
    character: Character = Character(author=user, **character_create.model_dump())
    await character.insert()
    return character


async def get_characters(user: user_model.User) -> List[Character]:
    """
    Get all characters for the given user.

    Args:
        user (user_model.User): The user whose characters to retrieve.

    Returns:
        List[Character]: A list of all the user's characters.
    """
    return await Character.find_all().to_list()
