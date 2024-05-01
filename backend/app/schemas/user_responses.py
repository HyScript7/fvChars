from pydantic import BaseModel


class JWTResponse(BaseModel):
    token: str
