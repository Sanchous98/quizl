from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas import User, UserCreate, UserUpdate
from dependencies import database
from db.crud import User as UserCRUD

router = APIRouter()


@router.post("/")
def create(user: UserCreate, db: Session = Depends(database)) -> User:
    db_user = UserCRUD.get_user_by_email(db, user.email)
    if db_user is not None:
        raise HTTPException(400, "Email already registered")

    return UserCRUD.register(db, user)


@router.get("/{user_id}")
def retrieve(user_id: int, db: Session = Depends(database)) -> User:
    db_user = UserCRUD.get(db, user_id)

    if db_user is None:
        raise HTTPException(400, "User not found")

    return db_user


@router.get("/")
def retrieve_all(db: Session = Depends(database)) -> List[User]:
    return UserCRUD.get_all(db)


@router.put("/{user_id}")
def update(user_id: int, user: UserUpdate, db: Session = Depends(database)) -> User:
    UserCRUD.update(db, user_id, user)

    return UserCRUD.get(db, user_id)


@router.delete("/{user}")
def delete(user: User, db: Session = Depends(database)):
    UserCRUD.drop(db, user.id)
