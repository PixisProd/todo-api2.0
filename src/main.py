from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from src import router
from src.database import create_tables, delete_tables


templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="ToDo 2.0",
    lifespan=lifespan
)


app.include_router(router)