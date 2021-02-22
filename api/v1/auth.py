import base64
import os
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


@router.post("/token", response_model=Token)
async def receive_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = repo.login(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE")))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout() -> RedirectResponse:
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="localtest.me")

    return response


@router.get("/login")
async def basic_auth(auth: BasicAuth = Depends(basic_auth)):
    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    try:
        decoded = base64.b64decode(auth).decode("ascii")
        username, _, password = decoded.partition(":")
        user = repo.login(username, password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE")))
        access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

        token = jsonable_encoder(access_token)

        response = RedirectResponse(url="/docs")
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            domain="localtest.me",
            httponly=True,
            max_age=1800,
            expires=1800,
        )
        return response

    except HTTPException:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)