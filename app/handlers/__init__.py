from aiogram import Router

from app.handlers import admin_command
from .base import router as base_router
from .callbacks import router as callback_router
from .create_order import router as create_order_router
from .admin_command import router as admin_command_router
from .order_admin import router as order_admin_router
from .panel import router as panel_router

router = Router()

router.include_router(base_router)
router.include_router(callback_router)
router.include_router(create_order_router)
router.include_router(admin_command_router)
router.include_router(order_admin_router)
router.include_router(panel_router)
