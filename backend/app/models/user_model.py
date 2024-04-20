from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped
from typing import List

from ..database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    characters = relationship("CharacterModel", backref="user")
    titles = relationship("TitleModel", backref="user")
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
