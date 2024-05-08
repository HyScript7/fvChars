from beanie import Document
from typing import List

from .user_model import User
from .character_model import Character

models: List[Document] = [User, Character]
