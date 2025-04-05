from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.todo.router import router as todo_router
from src.admin.router import router as admin_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(todo_router)
router.include_router(admin_router)