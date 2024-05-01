from datetime import datetime
from typing import Any, Optional

from beanie import Document
from pydantic import BaseModel, Field


class UserSignin(BaseModel):
    username: str = Field(description="The user's username")
    password: str = Field(description="The user's password")


class DisplaynameUpdate(BaseModel):
    displayname: Optional[str] = Field(
        default=None,
        description="The user's display name, which will be shown instead of their username",
    )


class PasswordUpdate(BaseModel):
    current_password: str = Field(description="The user's current password")
    new_password: str = Field(description="The user's desired password")


class UserSignup(UserSignin, DisplaynameUpdate):
    email: str = Field(description="The user's email address")


class UserPublic(BaseModel):
    userid: str = Field(description="The user's ID")
    username: str = Field(description="The user's username")
    displayname: str = Field(
        description="The user's display name, if there is one, otherwise their username",
    )
    created: datetime = Field(description="The user's creation time")


class User(Document):
    """
    A user document in the database.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email of the user.
        displayname (Optional[str]): The display name of the user.
    """
    username: str
    password: str
    email: str
    displayname: str

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"<User {self.username} {self.userid}>"

    def __str__(self) -> str:
        """
        Return the username, or displayname if set, of the User object.

        Returns:
            str: The name of the User object.
        """
        return self.name

    def __eq__(self, user: Any) -> bool:
        """
        Check if the User object is equal to another User object.

        Args:
            user (Any): The other User object.

        Returns:
            bool: True if the User objects are equal, False otherwise.
        """
        if not isinstance(user, User):
            return False
        return self.userid == user.userid

    def __hash__(self) -> int:
        """
        Return the hash of the User object.

        Returns:
            int: The hash of the User object.
        """
        return hash(self.userid)

    @property
    def userid(self) -> str | None:
        """
        Return the ID of the User object.

        Returns:
            str | None: The ID of the User object, or None if the object has not been saved to the database.
        """
        return self.id.binary.hex() if self.id else None

    @property
    def name(self) -> str:
        """
        Return the name of the User object.

        Returns:
            str: The name of the User object.
        """
        return self.displayname if self.displayname is not None else self.username

    @property
    def created(self) -> datetime | None:
        """
        Return the creation time of the User object.

        Returns:
            datetime | None: The creation time of the User object, or None if the object has not been saved to the database.
        """
        return self.id.generation_time if self.id else None
