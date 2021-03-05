from typing import List
from db.schemas import Rank
from fastapi import APIRouter
from dependencies import database
from db.repositories import User as UserRepository

router = APIRouter()
user_repo = UserRepository(next(database()))


@router.get("/{game_id}", response_model=List[Rank], responses={200: {"model": Rank}})
def per_game(game_id: int) -> List[Rank]:
    return user_repo.get_rankings(game_id)


@router.get("/", response_model=List[Rank], responses={200: {"model": Rank}})
def per_user() -> List[Rank]:
    return user_repo.get_rankings()

