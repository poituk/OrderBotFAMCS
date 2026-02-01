from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_menu_buttons() -> InlineKeyboardMarkup:
    keyboards_list = []
    keyboards_list.append(
        [InlineKeyboardButton(text="💰 Цены", callback_data="prices")]
    )
    keyboards_list.append(
        [InlineKeyboardButton(text="📦 Управление заказами", callback_data="order")]
    )
    keyboards_list.append(
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contact")]
    )
    keyboards_list.append([InlineKeyboardButton(text="❓ FAQ", callback_data="faq")])
    keyboard_menu = InlineKeyboardMarkup(inline_keyboard=keyboards_list)
    return keyboard_menu


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard_main = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/menu")], [KeyboardButton(text="/help")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard_main


def get_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="menu")]
        ]
    )


def order_keyboards() -> InlineKeyboardButton:
    keyboard = [
        [InlineKeyboardButton(text="➕ Сделать заказ", callback_data="set_order")],
        [InlineKeyboardButton(text="➖ Удалить заказ", callback_data="remove_order")],
        [InlineKeyboardButton(text="📋 Список заказов", callback_data="list_order")],
        [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def edit_keyboard() -> InlineKeyboardButton:
    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Изменить текст </start>", callback_data="edit_start"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Изменить текст <Контакты>", callback_data="edit_contact"
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Изменить текст <faq>", callback_data="edit_faq"
            )
        ],
        [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
