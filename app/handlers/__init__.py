from aiogram import Router
from .base import router as base_router
from .callbacks import router as callback_router
from .create_order import router as create_order_router

router = Router()

router.include_router(base_router)
router.include_router(callback_router)
router.include_router(create_order_router)
