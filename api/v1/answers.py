from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create():
    pass


@router.get("/{answer}")
def retrieve():
    pass


@router.get("/")
def retrieve_all():
    pass


@router.put("/{answer}")
def update():
    pass


@router.delete("/{answer}")
def delete():
    pass
