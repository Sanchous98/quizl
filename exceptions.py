from fastapi import HTTPException
from typing import Any, Optional, Dict


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = "Bad request", headers: Optional[Dict[str, Any]] = None):
        super().__init__(400, detail, headers)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: Any = "Unauthorized", headers: Optional[Dict[str, Any]] = None):
        super().__init__(401, detail, headers)


class ForbiddenException(HTTPException):
    def __init__(self, detail: Any = "Forbidden", headers: Optional[Dict[str, Any]] = None):
        super().__init__(403, detail, headers)
