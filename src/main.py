from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api import amazon_serv, war_service_live_serv, war_support_live_serv
from src.core.Logger import Logger
from src.core.setup import setup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager. Runs on startup and shutdown.
    """
    Logger().get().info("Application startup...")
    setup()
    yield
    Logger().get().info("Application shutdown...")


# Initialize the FastAPI app
app = FastAPI(
    lifespan=lifespan,
)


# Include the API router
app.include_router(amazon_serv.router)
app.include_router(war_service_live_serv.router)
app.include_router(war_support_live_serv.router)


@app.get("/docs")
async def redirect_to_docs():
    return RedirectResponse("/docs", status_code=308)


# @app.get("/")
# async def redirect_to_docs():
#     return RedirectResponse("/docs", status_code=308)
