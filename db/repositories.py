from sqlalchemy import func
from .models import Fillable
from . import models, schemas
from pydantic import BaseModel
from .schemas import UpdateBase
from sqlalchemy.orm import Session, Query
from typing import Type, TypeVar, Generic, Optional, List

modelType = TypeVar("modelType", bound=Fillable)
createSchema = TypeVar("createSchema", bound=BaseModel)
updateSchema = TypeVar("updateSchema", bound=UpdateBase)


class Repository(Generic[modelType, createSchema, updateSchema]):
    def __init__(self, db: Session, model: Type[modelType]):
        super().__init__()
        self.db = db
        self.model = model

    def __getitem__(self, model_id: int) -> modelType:
        return self.get(model_id)

    def __delitem__(self, model_id: int):
        self.drop(model_id)

    def __setitem__(self, model_id: int, schema: createSchema):
        if self.exists(model_id):
            self.update(model_id, schema)

        self.create(schema)

    def __iter__(self):
        return iter(self.all())

    def __reversed__(self):
        return reversed(self.all())

    def __contains__(self, model: modelType) -> bool:
        return self[model.id] == model

    def get(self, model_id: int) -> Optional[modelType]:
        return self.query().filter(self.model.id == model_id).first()

    def all(self, skip: int = 0, limit: Optional[int] = None) -> List[modelType]:
        query: Query = self.query().offset(skip)

        if limit is not None:
            query.limit(limit)

        return query.all()

    def create(self, schema: createSchema) -> modelType:
        instance: modelType = self.model()
        instance.fill(schema)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)

        return instance

    def update(self, model_id: int, schema: updateSchema):
        self.query().filter(self.model.id == model_id).update(schema.dict())

    def query(self, *entities) -> Query:
        return self.db.query(self.model, *entities)

    def exists(self, model_id: int) -> bool:
        return self.query().filter(self.model.id == model_id).exists()

    def drop(self, model_id: int):
        self.query().filter(self.model.id == model_id).delete()


class User(Repository[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.User)

    def login(self, username: str, hashed_password: str) -> Optional[modelType]:
        return self.query() \
            .filter(self.model.username == username and self.model.password == hashed_password) \
            .first()

    def create(self, schema: createSchema) -> modelType:
        instance: models.User = self.model()
        instance.fill(schema)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)

        return instance

    def get_by_username(self, username: str) -> Optional[modelType]:
        return self.query().filter(self.model.username == username).first()

    def get_by_email(self, email: str) -> Optional[modelType]:
        return self.query().filter(self.model.email == email).first()

    def soft_delete(self, user_id: int):
        self.query().filter(self.model.id == user_id).update({models.User.is_active: False})

    def get_rankings(self, game_id: Optional[int] = None):
        query: Query = self.query(func.sum(models.Question.points).label("points")) \
            .join(models.User.answers) \
            .join(models.Answer.question) \
            .join(models.Question.game) \
            .filter(models.Answer.right is True) \
            .group_by(models.Game.id) \
            .order_by("points")

        if game_id is not None:
            query.filter(models.Game.id == game_id)

        return query.all()


class Question(Repository[models.Question, schemas.QuestionCreate, schemas.QuestionUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Question)


class Answer(Repository[models.Answer, schemas.AnswerCreate, schemas.AnswerUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Answer)


class Game(Repository[models.Game, schemas.GameCreate, schemas.GameUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, models.Game)
