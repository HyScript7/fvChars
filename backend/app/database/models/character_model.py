from datetime import datetime
from typing import Any

from beanie import Document, Link

from . import user_model


class Character(Document):
    """
    A character document in the database.

    Attributes:
        author: (Link[User]): The user that the character belongs to.
        name (str): The name of the character
    """

    author: Link[user_model.User]
    name: str

    def __repr__(self) -> str:
        """
        Return a string representation of the Character object.

        Returns:
            str: A string representation of the Character object.
        """
        return f"<Character {self.name} {self.charid}>"

    def __str__(self) -> str:
        """
        Return the name of the Character object.

        Returns:
            str: The name of the Character object.
        """
        return self.name

    def __eq__(self, char: Any) -> bool:
        """
        Check if the Character object is equal to another Character object.

        Args:
            char (Any): The other Character object.

        Returns:
            bool: True if the Character objects are equal, False otherwise.
        """
        if not isinstance(char, Character):
            return False
        return self.charid == char.charid

    def __hash__(self) -> int:
        """
        Return the hash of the Character object.

        Returns:
            int: The hash of the Character object.
        """
        return hash(self.characterid)

    @property
    def charid(self) -> str | None:
        """
        Return the ID of the Character object.

        Returns:
            str | None: The ID of the Character object, or None if the object has not been saved to the database.
        """
        return self.id.binary.hex() if self.id else None

    @property
    def created(self) -> datetime | None:
        """
        Return the creation time of the Character object.

        Returns:
            datetime | None: The creation time of the Character object, or None if the object has not been saved to the database.
        """
        return self.id.generation_time if self.id else None

    @property
    def player(self) -> user_model.User:
        """Alias for `author`
        Return the user that the character belongs to.

        Returns:
            user_model.User: The user that the character belongs to.
        """
        return self.author
