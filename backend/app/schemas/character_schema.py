from typing_extensions import Optional
from pydantic import BaseModel, Field


class CharacterResponse(BaseModel):
    id: int
    userid: int
