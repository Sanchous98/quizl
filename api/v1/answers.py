from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create():
    pass


@router.get("/{answer}")
async def retrieve():
    pass


@router.get("/")
async def retrieve_all():
    pass


@router.put("/{answer}")
async def update():
    pass


@router.delete("/{answer}")
async def delete():
    pass
