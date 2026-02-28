
# dev build
```sh
uv venv
.venv\Scripts\activate
uv sync
```

# Running
```sh
uvicorn src.main:app --port 8001 --reload --log-level trace
```