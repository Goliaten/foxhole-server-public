from typing import Optional

from fastapi import APIRouter

from src.core.Logger import Logger


router = APIRouter(prefix="/war-service-live", tags=["war-service-live"])


@router.get("/", response_model=None)
@router.get("/{path:path}", response_model=None)
async def default_path(path: Optional[str] = ""):
    Logger().get().debug(f"/war-service-live/{path=}")
    return
