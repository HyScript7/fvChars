from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Session, get_db

app = FastAPI()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
