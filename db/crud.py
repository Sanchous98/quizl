from typing import List
from sqlalchemy.orm import Session
from . import models, schemas


class User:
    @staticmethod
    def get(db: Session, user_id: int) -> models.User:
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> models.User:
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def register(db: Session, user: schemas.UserCreate) -> models.User:
        db_user = models.User(email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def drop(db: Session, user_id: int):
        db.query(models.User).filter(models.User.id == user_id).delete()

    @staticmethod
    def soft_delete(db: Session, user_id: int):
        db.query(models.User).filter(models.User.id == user_id).update({models.User.is_active: False})

    @classmethod
    def update(cls, db: Session, user_id: int, user: schemas.UserUpdate):
        db.query(models.User).filter(models.User.id == user_id).update(user.dict())
