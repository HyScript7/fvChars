from sqlalchemy import Column, Integer, String, Boolean

from ..database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
