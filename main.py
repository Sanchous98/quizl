from api import api
from db import models
from fastapi import FastAPI
from db.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api.router, prefix="/api", tags=["api"])
