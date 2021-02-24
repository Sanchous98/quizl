from db.models import User, GamePlayer
from typing import Iterator
from fastapi import APIRouter
from dependencies import database
from exceptions import BadRequestException
from db.repositories import Game as GameRepository, User as UserRepository

router = APIRouter()
game_repo = GameRepository(next(database()))
user_repo = UserRepository(next(database()))


@router.get("/{game_id}")
def per_game(game_id: int):
    game_repo

    return


@router.get("/")
def per_user():
    players: Iterator[User] = map(lambda game: game.players, game_repo.all())


