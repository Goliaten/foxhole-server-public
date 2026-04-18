
# Table of Contents
- [Table of Contents](#table-of-contents)
- [Setup](#setup)
  - [dev build](#dev-build)
  - [altering .exe](#altering-exe)
  - [Running](#running)
- [Notes](#notes)
- [Order of requests](#order-of-requests)
- [Websocket order](#websocket-order)

# Setup
[to the top](#table-of-contents)

## dev build
```sh
docker compose down -v
docker compose up -d --build
```

## altering .exe
Open the `War-Win64-Shipping.exe` with Ghidra, and decompile it.
Change the `https://s3.amazonaws.com` into `http://localhost` in the string containing:
- `https://s3.amazonaws.com/foxhole-updates/newsfeed/news.json`
- `https://s3.amazonaws.com/foxhole-updates/config/client_config.json`

## Running
```sh
docker compose up -d
```

# Notes
[to the top](#table-of-contents)

- Other endpoints that exist in code code: `/socketExternal` and `/internal/worldconquest/`. Both of them replace `/external` at some point
- Other endpoints: `/modReply`, `modReply/acceptModReply`, `/report`, `/reportPlayer`, `/admincommand`
- Another API endpoint? `/warRecord/list` for `war-service-live` - `https://war-service-live.foxholeservices.com/external/warRecord/list`. Shows past war stats and achievment progress
{'url': 'http://localhost/war-service-live/warRecord/list', 'method': 'GET', 'path': 'warRecord/list', 'client_host': '172.19.0.2', 'headers': {'connection': 'Upgrade', 'host': 'localhost', 'content-length': '0', 'accept': '*/*', 'accept-encoding': 'deflate, gzip', 'user-agent': 'War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit'}, 'query_params': {}, 'body': None}
- The network architecture is assumed to be as follows. There are 2 kinds of servers: amazon and steam.
  Steam servers handle player connectivity, and amazon servers handle the metadata(?).
  So far, amazon servers have been found to provide the following data:
  - Information about what shards are available.
  - News feed
  - Starting data of the user
  - Authenticating player using steam-id and steam-token

# Order of requests
[to the top](#table-of-contents)

`{amazon-server}` is by default `https://s3.amazonaws.com`
- game launches
- request `GET` to `{amazon-server}/foxhole-updates/newsfeed/news.json` to get main page news
- request ? to `{amazon-server}/foxhole-updates/config/client_config.json` to get shard info, **war-service-live-server** and **war-support-live-server**
- click play
- request `GET` to `{war-service-live-server}warReportSummary`. There is no separator before warReportSummary. Most likely to fill up info about current war details. Although i haven't succeeded in querying this myself. #TODO do a manual query with specific headers
- request `GET` to `{war-service-live-server}`. The order of these exchanges will be described in [another chapter](#websocket-order)
  - This is a websocket connection. Subprotocol dictates the game version: `foxhole-warservice-client:1.63.41.x` for example.
  - Messages are encoded in FlatBuffers. It is assumed that root table has message_type and message_content inside it.
    - There are currently 15 message types discovered after brief testing:
      - 1 - client - initial message sent, contains steam-token and steam-id
      - 4 - server - response to initial message, contains a lot of data about user's current state (inventory, uniform. skin tone, activity log, spawn points)
      - 5 - client
      - 8 - server
      - 9 - server
      - 10 - client
      - 14a - server - long version
      - 14b - server - short version
      - 15 - server
      - 16 - client
      - 17 - server
      - 20 - client
      - 21 - server
      - 22 - client/server
      - 23 - client/server
  - Some messages have serialised FArchive within them.
  - Currently it is difficult to decode, alter, replicate these packets due to requirement of `.fbs` schema files for automated en-/decoding. Limited progress has been made in decoding message 1 and 4, however there is then a need for deserialising FArchive.
- request `GET` to `{war-support-live-server}/modReply`. Some checkup with user's data. Maybe VAC ban check or something.
  - specific headers: *x-steam-id*, *x-steam-token*
- In the background, connection by Steamworks is going on. At the beginning lot of 1300 long packets, then some 55 and 100 long packets are being transmitted between different steam servers. I assume that this is process by which steam server is chosen. After this is done, the chosen server will be the recipient of all later traffic when it comes to actually playing the game. I have been unable to find in the source code a URL that I can change to redirect all of these connections to my server. However, I have a clue. I can replace Steamworks API using the Goldberg Emulator.

# Websocket order
[to the top](#table-of-contents)

Format: {sender}{packet type}

1. c1 -> s4 -> c5 -> s9 -> s8
2. Then exchange loop with c24 <-> s24 for several packets
3. After that is an unknown order. Here are some observed events:
   - c23 <-> s23 exchange
   - constant stream of s14
   - constant, but sometimes interrupted stream of s15
   - c16 -> s17 response is not instant, but soon enough
   - c20 -> s21 response is not instant, but soon enough
