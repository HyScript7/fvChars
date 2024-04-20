from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from ..database import Base


class TitleModel(Base):
    __tablename__ = "titles"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.id"))
    title = Column(String, unique=True)

    def __init__(self, userid: int, title: str):
        self.userid = userid
        self.title = title
