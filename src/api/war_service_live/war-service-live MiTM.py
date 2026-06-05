import asyncio
import re
import websockets
import websockets.headers as wsh

from fastapi import Response, WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Request

from src.core.Logger import Logger
import src.config as cfg
from src.helpers.packer_analyzer import PacketAnalyzer

# HACK websockets module doesn't accept `:` as a valid character. This modifies the REGEX used in the module to allow semicolons
wsh._token_re = re.compile(r"[-!#$%&\':*+.^_`|~0-9a-zA-Z]+")

router = APIRouter(prefix="/war-service-live", tags=["war-service-live"])
# TODO make the base URL not constant
BASE_URL = "wss://war-service-live.foxholeservices.com/socketExternal"
DEFAULT_WEBSOCKET_PROTOCOL = "foxhole-warservice-client:1.63.41.x"


async def forward(source: WebSocket, destination: websockets.ClientConnection):
    """Forwards data from a FastAPI WebSocket to an external WebSocket."""
    try:
        while True:
            Logger().get().info("Receiving data from client")
            message = await source.receive()
            Logger().get().debug("Data received")

            if message.get("type") == "websocket.disconnect":
                Logger().get().info(
                    "Client sent `websocket.disconnect` message. Disconnecting from server"
                )
                await destination.close()
                break

            data = message["bytes"]
            opcode = PacketAnalyzer.get_packet_opcode(data)
            Logger().get().debug(
                f"client -> server FB opcode={opcode} len={len(data)} hexdata={data.hex()}"
            )
            Logger().get().info("Forwarding data to server")
            await destination.send(data)
            Logger().get().debug("Data forwarded")
    except Exception:
        import traceback

        Logger().get().error(f"Error: {traceback.format_exc()}")


async def reverse_forward(source: websockets.ClientConnection, destination: WebSocket):
    """Forwards data from an external WebSocket back to the FastAPI client."""
    try:
        while True:
            # FIXME after client disconnects, server can still send messages. Although this doesn't cause an issue, it makes an exception in logs
            Logger().get().info("Receiving data from server")
            data = await source.recv(decode=False)
            Logger().get().debug("Data received")

            opcode = PacketAnalyzer.get_packet_opcode(data)
            Logger().get().debug(
                f"server -> client FB opcode={opcode} len={len(data)} hexdata={data.hex()}"
            )
            Logger().get().info("Forwarding data to client")
            await destination.send_bytes(data)
            Logger().get().debug("Data forwarded")
    except Exception:
        import traceback

        Logger().get().error(f"Error: {traceback.format_exc()}")


@router.websocket("/")
async def default_websocket(websocket: WebSocket):
    Logger().get().info("Websocket /war-service-live/")
    await websocket.accept()
    Logger().get().debug("Accepted connection")

    Logger().get().debug(f"{websocket.headers=}")
    subprotocols = [
        websockets.Subprotocol(
            websocket.headers.get("sec-websocket-protocol", DEFAULT_WEBSOCKET_PROTOCOL)
        )
    ]
    if "sec-websocket-protocol" not in websocket.headers:
        Logger().get().error(
            f"`sec-websocket-protocol` header not found in client upgrade message. Defaulting to `{DEFAULT_WEBSOCKET_PROTOCOL}`"
        )
    else:
        Logger().get().info(f"Using subprotocols: {subprotocols}")

    # Establish connection to the external server
    try:
        async with websockets.connect(
            BASE_URL, subprotocols=subprotocols
        ) as external_ws:
            await asyncio.gather(
                forward(websocket, external_ws), reverse_forward(external_ws, websocket)
            )
    except WebSocketDisconnect:
        Logger().get().error("Client disconnected.")
    except Exception:
        import traceback

        Logger().get().error(f"Error: {traceback.format_exc()}")
    finally:
        # Ensure the local socket is closed if it hasn't been already
        try:
            await websocket.close()
            Logger().get().info("Closed websocket succesfully")
        except Exception:
            import traceback

            Logger().get().error("Unable to close websocket")
            Logger().get().error(traceback.format_exc())


# @router.api_route("/", response_model=None, methods=cfg.ALL_METHODS)
@router.api_route("/{path:path}", response_model=None, methods=cfg.ALL_METHODS)
async def default_path(request: Request, path: str) -> Response:
    Logger().get().debug(f"/war-service-live/{path=}")
    headers = dict(request.headers)

    query_params = dict(request.query_params)
    client_host = request.client.host if request.client else None

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
    return Response(status_code=204)
