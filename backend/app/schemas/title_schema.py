from pydantic import BaseModel


class TitleCreate(BaseModel):
    title: str


class TitleQuery(BaseModel):
    id: int


class TitleResponse(TitleCreate, TitleQuery):
    userid: int
