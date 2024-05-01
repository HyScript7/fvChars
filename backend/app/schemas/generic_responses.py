from pydantic import BaseModel

class GenericHTTPException(BaseModel):
    detail: str

class GenericMessageResponse(BaseModel):
    message: str
