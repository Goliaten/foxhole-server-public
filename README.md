
# Table of Contents
- [Table of Contents](#table-of-contents)
- [TODO](#todo)
- [Setup](#setup)
  - [dev build](#dev-build)
  - [altering .exe](#altering-exe)
  - [Running](#running)
- [Notes](#notes)
- [Order of requests](#order-of-requests)
- [Websocket order](#websocket-order)

# TODO
- [ ] test the following endpoint: request `GET` to `{war-service-live-server}warReportSummary`
- [ ] make a hooking mod with ue4ss on EVERY function to find out which one is responsible for data de-/serialization
- [x] dig into the game to find where serialization and deserialization happens
- [ ] mock server responses and launch the game with gbe emulator
- [x] replace IP in response 8 and see what happens
  - Hmm, replacing the IP seems to lock the game in a `waiting in queue` cycle after pressing deploy button.
- [ ] Perform deeper analysis, if we can mock the server behind IP in type 8 message
- [ ] keep mocking opcodes, see how far can we go with just replying with dummy messages
  - [x] op 4
  - [x] op 9
  - [x] op 8
  - [ ] op 23
  - [ ] and beyond
- [ ] Make a websocket for `{war-service-live-server}/shardStatus`

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
<!-- - `https://s3.amazonaws.com/foxhole-updates/newsfeed/news.json` -->
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
- Restarting server while the game is running, results in momentary message about foxhole services being unavailable.
- Replacing the IP in type 8 seems to lock the game in a `waiting in queue` cycle after pressing deploy button.

# Order of requests
[to the top](#table-of-contents)

`{amazon-server}` is by default `https://s3.amazonaws.com`
- game launches
- request `GET` to `{amazon-server}/foxhole-updates/newsfeed/news.json` to get main page news
- request ? to `{amazon-server}/foxhole-updates/config/client_config.json` to get shard info, **war-service-live-server** and **war-support-live-server**
- click play
- request `GET` to `{war-service-live-server}warReportSummary`. There is no separator before warReportSummary. Most likely to fill up info about current war details. Although i haven't succeeded in querying this myself.
- request `GET` to `{war-service-live-server}`. The order of these exchanges will be described in [another chapter](#websocket-order)
  - This is a websocket connection. Subprotocol dictates the game version: `foxhole-warservice-client:1.63.41.x` for example.
  - Messages are encoded in FlatBuffers. It is assumed that root table has message_type and message_content inside it.
    - These are the currently discovered message types discovered:
      - 1 - client - initial message sent, contains steam-token and steam-id
      - 3 - client - if first call to server(type 1) fails, client will sent type 3 without steam token (example in `foxhole_server_20260503114009.log`)
      - 4 - server - response to opcode 1 and 3, contains a lot of data about user's current state (inventory, uniform. skin tone, activity log, spawn points)
      - 5 - client
      - 6 - client - seems to be an empty keep-alive packet? Cacket sent after replacing IP in type 8 packet with a localhost, which caused the game to hand at `waiting in queue 0 players ahead` after clicking deploy.
      - 8 - server - IP inside this message points to a Hetzner data center in Falkenstein, Sachsen, Germany. Probably closest to my location. However why is it not pointing to steam servers? Pinging that IP results in no response.
      - 9 - server
      - 10 - client
      - 14a - server - long version
      - 14b - server - short version
      - 15 - server
      - 16 - client - related to opening map(?)
      - 17 - server - related to opening map(?)
      - 18 - client
      - 19 - server
      - 20 - client
      - 21 - server
      - 22 - client/server
      - 23 - client/server - related to getting data from server after entering region(?)
  - Some messages have serialised FArchive within them.
  - Currently it is difficult to decode, alter, replicate these packets due to requirement of `.fbs` schema files for automated en-/decoding. Limited progress has been made in decoding message 1 and 4, however there is then a need for deserialising FArchive.
- request `GET` to `{war-support-live-server}/modReply`. Some checkup with user's data. Maybe VAC ban check or something.
  - specific headers: *x-steam-id*, *x-steam-token*
- request `POST` to `{war-support-live-server}/modReply/acceptModReply'`. Log `foxhole_server_202603.log`
  - I have no idea how this was sent only once. However, this has caused me to display `null` message from time to time when logging in. This may be able to set something on the server, which `/modReply` then queries
  - full details:
```
[2026-03-24 23:17:02,375] [DEBUG|10] [war-support-live.py:default_path] {'url': 'http://localhost/war-support-live/modReply/acceptModReply', 'method': 'POST', 'path': 'modReply/acceptModReply', 'client_host': '172.19.0.1', 'headers': {'host': 'localhost', 'x-real-ip': '172.19.0.1', 'x-forwarded-for': '172.19.0.1', 'x-forwarded-proto': 'http', 'x-forwarded-host': 'localhost', 'x-forwarded-port': '80', 'connection': 'close', 'content-length': '27', 'accept': '*/*', 'accept-encoding': 'deflate, gzip', 'content-type': 'application/json', 'x-steam-id': '76561198222102524', 'x-steam-token': '<steam-token-replaced-for-security-concerns>', 'user-agent': 'War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit'}, 'query_params': {}, 'body': '{\r\n\t"ModMessage": "null"\r\n}'}
```
- request `PUT` to `{war-support-live-server}/report`. Log `foxhole_server_20260606202238.log`
  - specific headers: *x-steam-id*, *x-steam-token*, *user-agent*, *query_params*={}, *body*=`'{\r\n\t"EventType": "RegionConnectionAutoError",\r\n\t"Shard": 5,\r\n\t"Region": "HomeRegionW",\r\n\t"Faction": 1\r\n}'`
  - this was sent after dummy-ying opcodes 3,9,8, and passing through opcode 23, to which server returned `received 4001 (private use) Not authenticated; then sent 4001 (private use) Not authenticated`
  - full details:
```
{'url': 'http://localhost/war-support-live/report', 'method': 'PUT', 'path': 'report', 'client_host': '172.19.0.1', 'headers': {'host': 'localhost', 'x-real-ip': '172.19.0.1', 'x-forwarded-for': '172.19.0.1', 'x-forwarded-proto': 'http', 'x-forwarded-host': 'localhost', 'x-forwarded-port': '80', 'connection': 'close', 'content-length': '104', 'accept': '*/*', 'accept-encoding': 'deflate, gzip', 'content-type': 'application/json', 'x-steam-id': '76561198222102524', 'x-steam-token': '<steam-token-replaced-for-security-concerns>', 'user-agent': 'War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit'}, 'query_params': {}, 'body': '{\r\n\t"EventType": "RegionConnectionAutoError",\r\n\t"Shard": 5,\r\n\t"Region": "HomeRegionW",\r\n\t"Faction": 1\r\n}'}
```
- request `GET` to `{war-service-live-server}/shardStatus`. Log `foxhole_server_20260606202238.log`. Looks like websocket, with the following details: 
```
{'url': 'http://localhost/war-service-live/shardStatus', 'method': 'GET', 'path': 'shardStatus', 'client_host': '172.19.0.2', 'headers': {'connection': 'Upgrade', 'host': 'localhost', 'content-length': '0', 'accept': '*/*', 'accept-encoding': 'deflate, gzip', 'user-agent': 'War/++UE4+Release-4.24-CL-0 Windows/6.2.9200.1.256.64bit'}, 'query_params': {}, 'body': None}
```
- In the background, connection by Steamworks is going on. At the beginning lot of 1300 long packets, then some 55 and 100 long packets are being transmitted between different steam servers. I assume that this is process by which steam server is chosen. After this is done, the chosen server will be the recipient of all later traffic when it comes to actually playing the game. I have been unable to find in the source code a URL that I can change to redirect all of these connections to my server. However, I have a clue. I can replace Steamworks API using the Goldberg Emulator.

# Websocket order
[to the top](#table-of-contents)

Format: {sender}{packet type}
Senders:
- c - client
- s - server

1. c1 -> s4 -> c5 -> s9 -> s8
   1. if IP in s8 doesn't resolve properly, client sends back c6 packet
2. Then exchange loop with c23 <-> s23 for several packets
3. After that is an unknown order. Here are some observed events:
   - c22 <-> s22 exchange
   - constant stream of s14
   - constant, but sometimes interrupted stream of s15
   - c16 -> s17 response is not instant, but soon enough
   - c20 -> s21 response is not instant, but soon enough
