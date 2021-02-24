from typing import List
from dependencies import database
from api.middlewares import is_admin
from fastapi import APIRouter, Depends
from exceptions import BadRequestException
from starlette.responses import JSONResponse
from db.repositories import Game as GameRepository
from db.schemas import Game, GameCreate, GameUpdate

router = APIRouter()
repo = GameRepository(next(database()))


@router.post("/", dependencies=[Depends(is_admin)])
def create(game: GameCreate) -> Game:
    return repo.create(game)


@router.get("/{game_id}")
def retrieve(game_id: int) -> Game:
    db_game = repo.get(game_id)

    if db_game is None:
        raise BadRequestException("Game not found")

    return db_game


@router.get("/", dependencies=[Depends(is_admin)])
def retrieve_all() -> List[Game]:
    return repo.all()


@router.put("/{game_id}", dependencies=[Depends(is_admin)])
def update(game_id: int, game: GameUpdate) -> Game:
    db_game = repo.get(game_id)
    db_game.fill(game)

    return db_game


@router.delete("/{game_id}", dependencies=[Depends(is_admin)])
def delete(game_id: int):
    repo.drop(game_id)

    return JSONResponse()
