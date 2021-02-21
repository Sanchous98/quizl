from abc import ABC
from typing import List, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import UpdateBase


class Repository(ABC):
    def __init__(self, db: Session):
        self.db = db

    @property
    def model(self) -> Type[models.Fillable]:
        raise NotImplementedError

    def get(self, model_id: int) -> models.Fillable:
        return self.db.query(self.model).filter(self.model.id == model_id).first()

    def all(self, skip: int = 0, limit: int = 100) -> List[models.Fillable]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, schema: BaseModel) -> models.Fillable:
        instance = self.model()
        instance.fill(schema)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def update(self, model_id: int, schema: UpdateBase):
        self.db.query(self.model).filter(self.model.id == model_id).update(schema.dict())

    def drop(self, model_id: int):
        self.db.query(self.model).filter(self.model.id == model_id).delete()


class User(Repository):
    @property
    def model(self) -> Type[models.User]:
        return models.User

    def get(self, user_id: int) -> models.User:
        return super().get(user_id)

    def get_by_email(self, email: str) -> models.User:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def all(self, skip: int = 0, limit: int = 100) -> List[models.User]:
        return super().all(skip, limit)

    def create(self, user: schemas.UserCreate) -> models.User:
        return super().create(user)

    def soft_delete(self, user_id: int):
        return self.db.query(self.model).filter(self.model.id == user_id).update({models.User.is_active: False})

    def update(self, user_id: int, user: schemas.UserUpdate):
        super().update(user_id, user)


class Question(Repository):
    @property
    def model(self) -> Type[models.Question]:
        return models.Question

    def get(self, question_id: int) -> models.Question:
        return super().get(question_id)

    def all(self, skip: int = 0, limit: int = 100) -> List[models.Question]:
        return super().all(skip, limit)

    def add(self, question: schemas.QuestionCreate) -> models.Question:
        return super().create(question)

    def update(self, question_id: int, question: schemas.QuestionUpdate):
        super().update(question_id, question)
