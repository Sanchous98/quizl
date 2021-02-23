from typing import List, Type, TypeVar, Generic, Optional, overload
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models, schemas
from .models import Fillable
from .schemas import UpdateBase

modelType = TypeVar("modelType", bound=Fillable)
baseSchema = TypeVar("baseSchema", bound=BaseModel)
updateSchema = TypeVar("updateSchema", bound=UpdateBase)


class Repository(Generic[modelType, baseSchema, updateSchema]):
    def __init__(self, db: Session, model: Type[modelType]):
        self.db = db
        self.model = model

    def get(self, model_id: int) -> Optional[modelType]:
        return self.db.query(self.model).filter(self.model.id == model_id).first()

    def all(self, skip: int = 0, limit: int = 100) -> List[modelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, schema: baseSchema) -> modelType:
        instance = self.model()
        instance.fill(schema)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def update(self, model_id: int, schema: updateSchema):
        self.db.query(self.model).filter(self.model == model_id).update(schema.dict())

    def drop(self, model_id: int):
        self.db.query(self.model).filter(self.model.id == model_id).delete()


class User(Repository[models.User, schemas.UserBase, schemas.UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.User)

    def login(self, username: str, password: str) -> Optional[modelType]:
        return self.db.query(self.model).filter(self.model.username == username and self.model.password == password).first()

    def get_by_username(self, username: str):
        return self.db.query(self.model).filter(self.model.username == username)

    def get_by_email(self, email: str) -> Optional[modelType]:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def soft_delete(self, user_id: int):
        self.db.query(self.model).filter(self.model.id == user_id).update({models.User.is_active: False})


class Question(Repository[models.Question, schemas.QuestionBase, schemas.QuestionUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Question)


class Answer(Repository[models.Answer, schemas.AnswerBase, schemas.AnswerUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Answer)


class Game(Repository[models.Game, schemas.GameBase, schemas.GameUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Game)
