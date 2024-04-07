from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Session, get_db
from .routes.v1 import router as v1_router

app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
