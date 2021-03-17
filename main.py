import json
from typing import Union, TypeVar, Generic, Type

from api import api
from os import getenv
from db import models
from fastapi import FastAPI
from db.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(version=getenv("VERSION", "dev"), debug=getenv("DEBUG", False))
app.include_router(api.router, prefix="/api", tags=["API"])


anyType = TypeVar("anyType")


class X(Generic[anyType]):
    def __init__(self, value: anyType):
        self.value = value

    def get(self) -> anyType:
        return self.value


var = 10
a: anyType = 'aaa'
a: anyType = X(int).get()
