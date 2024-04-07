from pydantic import BaseModel


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

class UserSession(BaseModel):
    token: str
