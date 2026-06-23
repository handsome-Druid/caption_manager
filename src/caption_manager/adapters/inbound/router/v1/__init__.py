from fastapi import APIRouter

from .auto_remove import router as auto_remove_router

router = APIRouter()
router.include_router(auto_remove_router)

__all__ = [
    "router",
]
