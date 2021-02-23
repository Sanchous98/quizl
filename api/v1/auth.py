from base64 import b64decode
from os import getenv
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from starlette.responses import Response, RedirectResponse
from api.security import BasicAuth, basic_auth, Token, create_access_token
from db.repositories import User as UserRepository
from dependencies import database

router = APIRouter()
security = HTTPBasic()
repo = UserRepository(next(database()))


@router.post("/token")
def receive_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = repo.login(form_data.username, form_data.password)

    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE")))
    access_token = create_access_token({"sub": user.username}, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout() -> RedirectResponse:
    response = RedirectResponse(url="/docs")
    response.delete_cookie("Authorization", domain="localhost")

    return response


@router.get("/login")
def basic_auth(auth: BasicAuth = Depends(basic_auth)) -> RedirectResponse:
    headers: dict = {"WWW-Authenticate": "Basic"}

    if not auth:
        raise HTTPException(status_code=401, detail="Unauthorized", headers=headers)

    username, _, password = b64decode(auth).decode("ascii").partition(":")

    if repo.login(username, password) is None:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers=headers)

    access_token_expires = timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE")))
    access_token = create_access_token({"sub": username}, access_token_expires)

    response = RedirectResponse(url="/docs")
    response.set_cookie(
        "Authorization",
        value=f"Bearer {jsonable_encoder(access_token)}",
        domain="localhost",
        httponly=True,
        max_age=1800,
        expires=1800
    )

    return response

