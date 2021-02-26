from typing import List
from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from exceptions import BadRequestException
from starlette.responses import JSONResponse
from db.repositories import User as UserRepository
from db.schemas import User, UserCreate, UserUpdate

router = APIRouter()
repo = UserRepository(next(database()))


@router.post("/", response_model=User)
def create(user: UserCreate) -> User:
    if repo.get_by_email(user.email) is not None:
        raise BadRequestException("Email already registered")

    if repo.get_by_username(user.username) is not None:
        raise BadRequestException("Username already exists")

    return repo.create(user)


@router.get("/{user_id}")
def retrieve(user_id: int, additional_info: bool = Depends(is_admin)) -> dict:
    db_user = repo.get(user_id)

    if db_user is None:
        raise BadRequestException("User not found")

    response: dict = User.from_orm(db_user).dict()

    if additional_info:
        # Admin is able to view user's name and password hash
        response["username"] = db_user.username
        response["password"] = db_user.password

    return response


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
