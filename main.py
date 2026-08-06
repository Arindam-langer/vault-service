from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import routers
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    create_db_and_tables()
    yield
    logger.info("Shutting down application")


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(routers.router)
