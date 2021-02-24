from typing import List
from fastapi import APIRouter
from dependencies import database
from exceptions import BadRequestException
from starlette.responses import JSONResponse
from db.repositories import User as UserRepository
from db.schemas import User, UserCreate, UserUpdate

router = APIRouter()
repo = UserRepository(next(database()))


@router.post("/")
def create(user: UserCreate) -> User:
    if repo.get_by_email(user.email) is not None:
        raise BadRequestException("Email already registered")

    if repo.get_by_username(user.username) is not None:
        raise BadRequestException("Username already exists")

    return repo.create(user)


@router.get("/{user_id}")
def retrieve(user_id: int) -> User:
    db_user = repo.get(user_id)

    if db_user is None:
        raise BadRequestException("User not found")

    return db_user


@router.get("/")
def retrieve_all() -> List[User]:
    return repo.all()


@router.put("/{user_id}")
def update(user_id: int, user: UserUpdate) -> User:
    db_user = repo.get(user_id)
    db_user.fill(user)

    return db_user


@router.delete("/{user_id}")
def delete(user_id: int):
    repo.drop(user_id)

    return JSONResponse()
