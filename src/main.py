import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.api import wars
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
    logger.info("Application startup...")
    yield
    logger.info("Application shutdown...")


# Initialize the FastAPI app
app = FastAPI(
    lifespan=lifespan,
)

# Include the API router
app.include_router(wars.router, tags=[])

# @app.get("/")
# async def redirect_to_docs():
#     return RedirectResponse("/docs", status_code=308)
