import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.app.api.v1 import wars
from src.app.core.config import settings

# Set up logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Polling interval (in seconds)
POLL_INTERVAL = 300  # 5 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager. Runs on startup and shutdown.
    """
    # On startup
    logger.info("Application startup...")

    yield  # The application is now running

    # On shutdown
    logger.info("Application shutdown...")


# Initialize the FastAPI app
app = FastAPI(
    title="learning_tracker API",
    description="Platform for tracking learning progress",
    version="0.1.0",
    lifespan=lifespan,
)

# Include the API router
app.include_router(wars.router, tags=[])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs", status_code=308)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}
