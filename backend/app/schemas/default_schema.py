from typing import Any
from pydantic import BaseModel

class GenericHTTPException(BaseModel):
    detail: str
