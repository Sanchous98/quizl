from sqlalchemy import func

from .models import Fillable
from . import models, schemas
from pydantic import BaseModel
from .schemas import UpdateBase
from sqlalchemy.orm import Session, Query
from typing import List, Type, TypeVar, Generic, Optional

modelType = TypeVar("modelType", bound=Fillable)
baseSchema = TypeVar("baseSchema", bound=BaseModel)
updateSchema = TypeVar("updateSchema", bound=UpdateBase)


class Repository(Generic[modelType, baseSchema, updateSchema]):
    def __init__(self, db: Session, model: Type[modelType]):
        self.db = db
        self.model = model

    def get(self, model_id: int) -> Optional[modelType]:
        return self.query().filter(self.model.id == model_id).first()

    def all(self, skip: int = 0, limit: int = 100) -> List[modelType]:
        return self.query().offset(skip).limit(limit).all()

    def create(self, schema: baseSchema) -> modelType:
        instance: modelType = self.model()
        instance.fill(schema)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)

        return instance

    def update(self, model_id: int, schema: updateSchema):
        self.query().filter(self.model == model_id).update(schema.dict())

    def drop(self, model_id: int):
        self.query().filter(self.model.id == model_id).delete()

    def query(self) -> Query:
        return self.db.query(self.model)


class User(Repository[models.User, schemas.UserBase, schemas.UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.User)

    def login(self, username: str, hashed_password: str) -> Optional[modelType]:
        return self.db.query(self.model) \
            .filter(self.model.username == username and self.model.password == hashed_password) \
            .first()

    def create(self, schema: schemas.UserCreate) -> modelType:
        instance: models.User = self.model()
        instance.fill(schema)
        instance.is_active = False
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)

        return instance

    def get_by_username(self, username: str):
        return self.db.query(self.model).filter(self.model.username == username)

    def get_by_email(self, email: str) -> Optional[modelType]:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def soft_delete(self, user_id: int):
        self.db.query(self.model).filter(self.model.id == user_id).update({models.User.is_active: False})

    def get_points_by_user(self, game_id: Optional[int] = None) -> list[modelType]:
        query: Query = self.db.query(self.model, func.sum(models.Question.points).label("points"))\
            .join(models.User.answers)\
            .join(models.Answer.question)\
            .join(models.Question.game)\
            .filter(models.Answer.right is True)\
            .group_by(models.Game.id)\
            .order_by("points")\

        if game_id is not None:
            query.filter(models.Game.id == game_id)

        return query.all()



class Question(Repository[models.Question, schemas.QuestionBase, schemas.QuestionUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Question)


class Answer(Repository[models.Answer, schemas.AnswerBase, schemas.AnswerUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Answer)


class Game(Repository[models.Game, schemas.GameBase, schemas.GameUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Game)
