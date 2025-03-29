from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.auth.router import router as auth_router
from src.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    title="ToDo 2.0",
    lifespan=lifespan
)

app.include_router(router=auth_router)