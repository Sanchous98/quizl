from fastapi import Depends, HTTPException
from .security import get_current_active_user
from db.models import User


async def is_admin(user: User = Depends(get_current_active_user)):
    if not user.is_super:
        raise HTTPException(status_code=403, detail="Forbidden")
