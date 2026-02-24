# Platform for tracking learning progress API

It uses FastAPI, SQLAlchemy (async), `uv` for package management, and `ruff` for linting/formatting.

## 1. Prerequisites

* [**Docker**](https://www.docker.com/get-started) and **Docker Compose**
* [**`uv`**](https://github.com/astral-sh/uv) (Python package manager)

## 2. Setup & Installation

### Step 1: Clone and Set Up Environment

1.  Clone this repository.
2.  Navigate into the project directory.
3.  Create your `.env` file:
    ```bash
    cp .env.example .env
    ```
4.  **Edit `.env`** and set your `MARIADB_ROOT_PASSWORD` and other variables. The defaults should work for a local setup.

### Step 2: Start the MariaDB Database

Run the Docker Compose file to start the MariaDB container in the background.

```bash
docker compose -f docker-compose.yml up -d
```

### Step 3: Setup the database tables

Create the database structure from .sql file.
Change mysecretpassword and fochole_war_db if you changed them in .env file.

```bash
docker exec -i learning_tracker_mariadb mariadb -uroot -pmysecretpassword foxhole_war_db < bb.sql
```

### Step 4: Python virtual environment.

Use uv to create and install venv.

```bash
uv venv & uv sync
```

For development use the following to install dev packages
```bash
uv sync -group dev
```

## 3. Launching the server
### 1. Activating python's venv
On windows:
```bash
.venv\Scripts\activate
```

On linux:
```bash
source .venv/bin/activate
```

### 2. Starting the server
```bash
uvicorn src.app.main:app --reload
```

## 4. Endpoints
Documentation for all endpoints is available at `/docs` endpoint.