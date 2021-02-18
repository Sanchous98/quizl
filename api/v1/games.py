from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create():
    pass


@router.get("/{game}")
async def retrieve():
    pass


@router.get("/")
async def retrieve_all():
    pass


@router.put("/{game}")
async def update():
    pass


@router.delete("/{game}")
async def delete():
    pass
