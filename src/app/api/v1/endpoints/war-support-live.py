from fastapi import APIRouter


router = APIRouter(prefix="/war-support-live", tags=["war-support-live"])


@router.get("/{path:path}", response_model=None)
async def default_path(path):
    print(f"{path=}")
    return
