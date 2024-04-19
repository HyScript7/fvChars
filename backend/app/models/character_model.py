from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from ..database import Base

class CharacterModel(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'))
    def __init__(self, userid):
        self.userid = userid
