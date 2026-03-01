
# dev build
```sh
uv venv
.venv\Scripts\activate
uv sync
```

# altering .exe
Open the `War-Win64-Shipping.exe` with Ghidra, and decompile it.
Change `http` to `https` in:
- `https://s3.amazonaws.com/foxhole-updates/newsfeed/news.json`
- `https://s3.amazonaws.com/foxhole-updates/config/client_config.json`
Or you could change the entire URL to direct to localhost.

# Running
```sh
uvicorn src.main:app --port 8001 --reload --log-level trace
```

# Notes
- Attempting to set up https server with trusted certification failed. Had to resolve to modifying binary and pointing to localhost. However even when returning whatever the amazon server sends, game fails to connect. To investigate if there is something else that amazon server returns and we dont see. Perhaps fill up the warServiceExternalURL/external/warReportSummary with some data to see if it starts up.