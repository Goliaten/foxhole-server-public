
# dev build
```sh
docker compose down -v
docker compose up -d --build
```

# altering .exe
Open the `War-Win64-Shipping.exe` with Ghidra, and decompile it.
Change `http` to `https` in:
- `https://s3.amazonaws.com/foxhole-updates/newsfeed/news.json`
- `https://s3.amazonaws.com/foxhole-updates/config/client_config.json`

Or you could change the entire URL to direct to localhost.

# Running
```sh
docker compose up -d
```

# Notes
- Attempting to set up https server with trusted certification failed. Had to resolve to modifying binary and pointing to localhost. However even when returning whatever the amazon server sends, game fails to connect. To investigate if there is something else that amazon server returns and we dont see. Perhaps fill up the warServiceExternalURL/external/warReportSummary with some data to see if it starts up.
- #TODO make default endpoints forward all data to the desired server, and see what comes out
- Forwarding data to https server after receiving it with http didn't work. Remote server keeps sending 404 errors, even after sending messages to the same endpoints as the game.
- Attempted a MiTM Proxy. Didnt work. Client spews that TLS handshake failed due to untrusted certificate: "SSL error: unable to get local issuer certificate (preverify_ok=0;err=20;depth=0)". Tried changing the return of function printing this out, but it didn't help. Most likely didn't change it properly.
- Other endpoints that exist in code code: `/socketExternal` and `/internal/worldconquest/`. Both of them replace `/external` at some point
- Other endpoints: `/modReply`, `modReply/acceptModReply`, `/report`, `/reportPlayer`, `/admincommand`
- Another API endpoint? `/warRecord/list` for `war-service-live` - `https://war-service-live.foxholeservices.com/external/warRecord/list`. Shows past war stats and chievment progress
{'url': 'http://localhost/war-service-live/warRecord/list', 'method': 'GET', 'path': 'warRecord/list', 'client_host': '172.19.0.2', 'headers': {'connection': 'Upgrade', 'host': 'localhost', 'content-length': '0', 'accept': '*/*', 'accept-encoding': 'deflate, gzip', 'user-agent': 'War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit'}, 'query_params': {}, 'body': None}

# Order of requests
`{amazon-server}` is by default `https://s3.amazonaws.com`
- game launches
- request `GET` to `{amazon-server}/foxhole-updates/newsfeed/news.json` to get main page news
- request ? to `{amazon-server}/foxhole-updates/config/client_config.json` to get shard info, **war-service-live-server** and **war-support-live-server**
- click play
- request `GET` to `{war-service-live-server}warReportSummary`. There is no separator before warReportSummary. Most likely to fill up info about current war details. Although i haven't succeeded in querying this myself. #TODO do a manual query with specific headers
- request `GET` to `{war-service-live-server}`. Looking at the headers, it's something about establishing a WebSocket connection to a server.
  - specific headers: *sec-websocket-key*, *sec-websocket-protocol*, *sec-websocket-extensions*, *sec-websocket-version*
  - websocket extensions: `permessage-deflate; client_max_window_bits; client_no_context_takeover; server_no_context_takeover`
  - Game seems to be using https://libwebsockets.org/ websocket, as on failed connection it prints `LogLwsWebSockets: Warning: Lws(Warning): lws_client_handshake: got bad HTTP response '404'\n LogClient: Error: FExternalWarService::OnConnectionError Unable to connect` into console.
  - After connecting it sends some token, and steam-id in a byte stream.
  - Replacing `/external` with `/socketExternal` and connecting to websocket returns non 404 errors
    - subprotocol header has to be with version. otherwise we get error 4000.
    - some data sent will not return anything
    - sending the data, that was received from the game returns 4002 #TODO experiment with this
- request `GET` to `{war-support-live-server}/modReply`. Some checkup with user's data. Maybe VAC ban check or something.
  - specific headers: *x-steam-id*, *x-steam-token*
