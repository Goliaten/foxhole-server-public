from typing import Optional

from fastapi import APIRouter

from src.core.Logger import Logger


router = APIRouter(prefix="/war-support-live", tags=["war-support-live"])


@router.get("/", response_model=None)
@router.get("/{path:path}", response_model=None)
async def default_path(path: Optional[str] = ""):
    Logger().get().debug(f"/war-support-live/{path=}")
    return
