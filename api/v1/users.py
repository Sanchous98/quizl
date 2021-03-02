from typing import Union
from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from db.repositories import User as UserRepository
from exceptions import BadRequestException, ExceptionScheme
from db.schemas import User, UserCreate, UserUpdate, UserBase

router = APIRouter()
repo = UserRepository(next(database()))


@router.post("/", response_model=User, responses={200: {"model": User}, 400: {"model": ExceptionScheme}})
def create(user: UserCreate) -> User:
    if repo.get_by_email(user.email) is not None:
        raise BadRequestException("Email already registered")

    if repo.get_by_username(user.username) is not None:
        raise BadRequestException("Username already exists")

    return repo.create(user)


@router.get(
    "/{user_id}",
    response_model=UserCreate,
    responses={200: {"model": Union[User, UserCreate]}, 400: {"model": ExceptionScheme}}
)
def retrieve(user_id: int, additional_info: bool = Depends(is_admin)) -> UserBase:
    db_user = repo.get(user_id)

    if db_user is None:
        raise BadRequestException("User not found")

    if additional_info:
        # Admin is able to view user's name and password hash
        return UserCreate.from_orm(db_user)

    return User.from_orm(db_user)


@router.get("/", response_model=list[User], responses={200: {"model": list[User]}})
def retrieve_all() -> list[User]:
    return repo.all()


@router.put("/{user_id}", response_model=User, responses={200: {"model": User}})
def update(user_id: int, user: UserUpdate) -> User:
    db_user = repo.get(user_id)
    db_user.fill(user)

    return db_user


@router.delete("/{user_id}")
def delete(user_id: int):
    repo.drop(user_id)

    return JSONResponse()
