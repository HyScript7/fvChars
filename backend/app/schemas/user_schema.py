from typing_extensions import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str


class UserSignup(UserBase):
    password: str
    email: str


class UserSignin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    email: str


class UserToken(BaseModel):
    token: Optional[str] = Field(None, description="JWT token or None if Guest")


class UserSession(UserResponse, UserToken):
    pass
