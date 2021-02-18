from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create():
    pass


@router.get("/{question}")
async def retrieve():
    pass


@router.get("/")
async def retrieve_all():
    pass


@router.put("/{question}")
async def update():
    pass


@router.delete("/{question}")
async def delete():
    pass
