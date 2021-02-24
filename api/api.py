from .v1 import api
from fastapi import APIRouter

router = APIRouter()
router.include_router(api.router, prefix="/v1", tags=["v1"])
