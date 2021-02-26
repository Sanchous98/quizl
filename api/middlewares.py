from db.models import User
from fastapi import Depends
from exceptions import ForbiddenException
from .security import get_current_active_user


async def is_admin(user: User = Depends(get_current_active_user)):
    if not user.is_super:
        raise ForbiddenException()
