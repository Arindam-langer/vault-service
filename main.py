from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(routers.router)
