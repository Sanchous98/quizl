from fastapi import APIRouter
from api.v1 import api

router = APIRouter()
router.include_router(api.router, prefix="/v1", tags=["v1"])
