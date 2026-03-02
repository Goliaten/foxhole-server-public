
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

# Order of requests
`{amazon-server}` is by default `https://s3.amazonaws.com`
- game launches
- request `GET` to `{amazon-server}/foxhole-updates/newsfeed/news.json` to get main page news
- request ? to `{amazon-server}/foxhole-updates/config/client_config.json` to get shard info, **war-service-live-server** and **war-support-live-server**
- click play
- request `GET` to `{war-service-live-server}warReportSummary`. There is no separator before warReportSummary. Most likely to fill up info about current war details. Although i haven't succeeded in querying this myself. #TODO do a manual query with specific headers
- request `GET` to `{war-service-live-server}`. Looking at the headers, it's something about establishing a WebSocket connection to a server.
  - specific headers: *sec-websocket-key*, *sec-websocket-protocol*, *sec-websocket-extensions*, *sec-websocket-version*
- request `GET` to `{war-support-live-server}/modReply`. Some checkup with user's data. Maybe VAC ban check or something.
  - specific headers: *x-steam-id*, *x-steam-token*
This is as far as I've analysed. Next the client will try to make a connection to `{war-service-live-server}` over and over. #TODO experiment with this endpoint