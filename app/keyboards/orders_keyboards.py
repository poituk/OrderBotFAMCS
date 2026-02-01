from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils import keyboard

def get_orders_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Список заказов", callback_data="orders_admin_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🕰️ Самый старый заказ", callback_data="old_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔥 Последний заказ", callback_data="last_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✔️ Выполнить заказ", callback_data="сomplete_order"
                )
            ],
            [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="menu")],
        ]
    )
    return keyboard


def get_back_orders() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в меню заказов", callback_data="back_orders")]
        ]
    )


def complete_orders() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🥇 Выполнить самый старый заказ", callback_data="complete_first"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Выполнить последний заказ", callback_data="complete_last"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔢 Выполнить по номеру заказа",
                    callback_data="complete_number",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться в меню заказов", callback_data="back_orders"
                )
            ],
        ]
    )
    return keyboard
