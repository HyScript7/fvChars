from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .models import models


async def database_setup(app: FastAPI):
    app.db = AsyncIOMotorClient("mongodb://root:root@localhost:27017")
    await init_beanie(database=app.db.get_database("fvchars"), document_models=models)
