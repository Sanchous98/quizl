from os import getenv
from jwt import encode
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2
from starlette.requests import Request
from datetime import datetime, timedelta
from exceptions import UnauthorizedException
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = "", auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.model = SecurityBase()

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise UnauthorizedException(detail="Unauthorized")
            else:
                return None

        return param


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(self, token_url: str,
                 scheme_name: Optional[str] = None,
                 scopes: Optional[dict] = None,
                 auto_error: bool = True):
        if scopes is None:
            scopes = {}

        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=token_url, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")
        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param
        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False
            scheme = param = ""

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None

        return param


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    copy = data.copy()
    copy.update({"exp": datetime.utcnow() + expires_delta})

    return encode(copy, getenv("SECRET_KEY"))
