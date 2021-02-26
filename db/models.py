from .database import Base
from pydantic import BaseModel
from typing import TypeVar, Generic
from dependencies import hash_password
from sqlalchemy.orm import relationship
from .schemas import UserBase, GameBase, QuestionBase, AnswerBase
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, SmallInteger, DateTime, func, Table

modelType = TypeVar("modelType", bound=BaseModel)
users_games = Table(
    'users_games', Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False, primary_key=True),
    Column("game_id", Integer, ForeignKey("games.id"), nullable=False, primary_key=True)
)
players_answers = Table(
    "players_answers", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False, primary_key=True),
    Column("game_id", Integer, ForeignKey("games.id"), nullable=False, primary_key=True),
    Column("answer_id", Integer, ForeignKey("answers.id"), nullable=False, primary_key=True)
)


class Fillable(Generic[modelType]):
    id = Column(Integer, primary_key=True)

    def fill(self, schema: modelType):
        for key, value in schema.dict().items():
            if value is not None:
                self.__setattr__(key, value)


class User(Fillable[UserBase], Base):
    __tablename__ = "users"

    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_super = Column(Boolean, default=False, nullable=False)
    games = relationship("Game", back_populates="players", secondary=users_games)
    answers = relationship("Answer", back_populates="players", secondary=players_answers)

    def fill(self, schema: modelType):
        super().fill(schema)
        self.password = hash_password(self.password)


class Game(Fillable[GameBase], Base):
    __tablename__ = "games"

    players = relationship("User", back_populates="games", secondary=users_games)
    questions = relationship("Question", back_populates="game")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    finishes_at = Column(DateTime, nullable=True)


class Question(Fillable[QuestionBase], Base):
    __tablename__ = "questions"

    text = Column(Text, nullable=False)
    points = Column(SmallInteger, nullable=False, default=1)
    answers = relationship("Answer", back_populates="question")
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship("Game", back_populates="questions")


class Answer(Fillable[AnswerBase], Base):
    __tablename__ = "answers"

    text = Column(Text, nullable=False)
    right = Column(Boolean, default=False, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship("Question", back_populates="answers")
    players = relationship("User", back_populates="answers", secondary=players_answers)
