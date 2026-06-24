from fastapi import APIRouter

from .auto_remove import router as auto_remove_router
from .check_captions import router as check_captions_router
from .custom_remove import router as custom_remove_router

router = APIRouter()
router.include_router(auto_remove_router)
router.include_router(check_captions_router)
router.include_router(custom_remove_router)

__all__ = [
    "router",
]
