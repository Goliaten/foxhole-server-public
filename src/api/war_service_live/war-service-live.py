from typing import Optional
from fastapi import APIRouter, Request, WebSocket

from src.core.Logger import Logger
import src.config as cfg

router = APIRouter(prefix="/war-service-live", tags=["war-service-live"])
BASE_URL = "https://war-service-live.foxholeservices.com/external"


@router.websocket("/")
async def default_websocket(websocket: WebSocket):
    Logger().get().info("Websocket /war-service-live/")
    Logger().get().debug(f"{websocket.headers=}")
    Logger().get().debug(f"{websocket.base_url=}")
    Logger().get().debug(f"{websocket.query_params=}")
    Logger().get().debug(f"{websocket.path_params=}")
    await websocket.accept(subprotocol="foxhole-warservice-client:1.63.40.x")

    Logger().get().debug("Accepted. Receiving data")
    try:
        while True:
            to_send = None
            Logger().get().debug("Receiving data")
            message = await websocket.receive()
            if message["type"] == "websocket.receive":
                if "text" in message:
                    to_send = message["text"]
                    Logger().get().debug(f"Received text: {to_send}")
                elif "bytes" in message:
                    to_send = message["bytes"]
                    Logger().get().debug(f"Received bytes: {to_send}")
                else:
                    Logger().get().debug(f"Received unknown message: {message}")
            elif message["type"] == "websocket.disconnect":
                Logger().get().debug(
                    f"Client disconnected with code: {message.get('code', 'unknown')}"
                )
                break
            else:
                Logger().get().debug(
                    f"Received message type: {message['type']}, data: {message}"
                )

            if to_send:
                ...
    except Exception as e:
        import traceback

        traceback.print_exc()

    Logger().get().info("Client disconnected from websocket.")


# @router.api_route("/", response_model=None, methods=cfg.ALL_METHODS)
@router.api_route("/{path:path}", response_model=None, methods=cfg.ALL_METHODS)
async def default_path(request: Request, path: str):
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
