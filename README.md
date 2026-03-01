
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