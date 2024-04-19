from app import app
from app.database import Base, engine
from app.models import *
from fastapi.testclient import TestClient

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)
