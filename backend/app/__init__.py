from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import database_setup


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_setup(app)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}
