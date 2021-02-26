from fastapi import APIRouter
from dependencies import database
from db.repositories import User as UserRepository

router = APIRouter()
user_repo = UserRepository(next(database()))


@router.get("/{game_id}")
def per_game(game_id: int):
    return user_repo.get_rankings(game_id)


@router.get("/")
def per_user():
    return user_repo.get_rankings()

