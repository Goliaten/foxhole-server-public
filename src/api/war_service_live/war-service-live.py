from typing import Optional
from fastapi import APIRouter, Request, WebSocket

from src.core.Logger import Logger
import src.config as cfg

router = APIRouter(prefix="/war-service-live", tags=["war-service-live"])


# @router.api_route("/", response_model=None, methods=cfg.ALL_METHODS)
@router.api_route("/{path:path}", response_model=None, methods=cfg.ALL_METHODS)
async def default_path(request: Request, path: Optional[str] = ""):
    Logger().get().debug(f"/war-service-live/{path=}")
    headers = dict(request.headers)

    # Query parameters
    query_params = dict(request.query_params)

    # Client IP (if behind a proxy, use X-Forwarded-For)
    client_host = request.client.host if request.client else None

    # Body (only for POST, PUT, PATCH, etc.)
    body = None
    try:
        body = await request.body()
        body = body.decode("utf-8") if body else None
    except Exception as e:
        body = f"Error reading body: {e}"

    # URL and method
    url = str(request.url)
    method = request.method
    Logger().get().debug(
        {
            "url": url,
            "method": method,
            "path": path,
            "client_host": client_host,
            "headers": headers,
            "query_params": query_params,
            "body": body,
        }
    )
    return


@router.websocket("/")
async def default_websocket(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except Exception as e:
        import traceback

        traceback.print_exc()

    print("Client disconnected")
