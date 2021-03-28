from api import api
from db import models
from fastapi import FastAPI
from db.database import engine
from os import getenv, mkdir, curdir

try:
    mkdir(curdir + "/var")
except FileExistsError:
    pass

models.Base.metadata.create_all(bind=engine)
app = FastAPI(version=getenv("VERSION", "dev"), debug=getenv("DEBUG", False))
app.include_router(api.router, prefix="/api", tags=["API"])
