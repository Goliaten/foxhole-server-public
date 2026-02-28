from fastapi import APIRouter


router = APIRouter(prefix="/war-service-live", tags=["war-service-live"])


@router.get("/{path:path}", response_model=None)
async def default_path(path):
    print(f"{path=}")
    return
