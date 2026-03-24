import asyncio
import re
import websockets
import websockets.headers as wsh

# import websockets.extensions as wse
import websockets.extensions.permessage_deflate
import time


async def connect():
    uri = "wss://war-service-live.foxholeservices.com/socketExternal"
    wsh._token_re = re.compile(r"[-!#$%&\':*+.^_`|~0-9a-zA-Z]+")

    # Define your custom headers
    extra_headers = {
        # "user-agent": "War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit",
        # "Sec-WebSocket-Protocol": "foxhole-warservice-client:1.63.40.x",
        "sec-websocket-key": "Zb0MS3zRCewP9Eh24HQyug=="
    }

    # Define your subprotocols
    subprotocols = ["foxhole-warservice-client:1.63.40.x"]
    extensions = [
        websockets.extensions.permessage_deflate.ClientPerMessageDeflateFactory(
            True, True
        )
    ]

    async with websockets.connect(
        uri,
        additional_headers=extra_headers,
        subprotocols=subprotocols,
        extensions=extensions,
        origin="https://war-service-live.foxholeservices.com",
    ) as websocket:
        # websocket.sub
        print("Connected!")
        data = b""
        [x.decode() for x in data]
        await websocket.send(data)
        response = await websocket.recv()
        print(response)
        # Your logic here


asyncio.run(connect())

while True:
    time.sleep(1)
