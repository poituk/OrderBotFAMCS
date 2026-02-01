from email import message
from aiogram import F, Router
from aiogram.dispatcher import router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile, InputFile
from datetime import datetime

from aiogram.enums import ParseMode

from app.database.crud_order import get_orders, remove_order
from app.responses import CONTACTS, FAQ
from app.keyboards.keyboards import get_back_menu, get_menu_buttons, order_keyboards

router = Router()


class OrderStates(StatesGroup):
    del_order = State()


@router.callback_query(F.data == "prices")
async def get_prices(callback: CallbackQuery):
    file_path = "documents/services.pdf"
    await callback.message.answer("Цена на наши услуги: ")
    await callback.message.answer_document(
        FSInputFile(file_path), reply_markup=get_back_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "contact")
async def get_contact(callback: CallbackQuery):
    result = "<b>Наши контакты:</b>\n\n"
    for key, value in CONTACTS.items():
        result += f"<b>{key}</b> : {value}\n\n"
    await callback.message.answer(
        text=result, parse_mode=ParseMode.HTML, reply_markup=get_back_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "faq")
async def get_faq(callback: CallbackQuery):
    result = "<b>Часто задаваемые вопросы:</b>\n\n"
    for val in FAQ:
        result += f"<b>Q: {val[0]}</b>\n A: {val[1]}\n\n"
    await callback.message.answer(
        text=result, parse_mode=ParseMode.HTML, reply_markup=get_back_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "menu")
async def menu_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    photo = FSInputFile("img/logo.jpg")
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=get_menu_buttons(),
    )

    await callback.answer()


@router.callback_query(F.data == "order")
async def get_order_operation(callback: CallbackQuery):
    await callback.message.answer(
        "<b>Выберите тип оперпции:</b>", reply_markup=order_keyboards()
    )
    await callback.answer()


@router.callback_query(F.data == "list_order")
async def admin_list(callback: CallbackQuery):
    all_orders = await get_orders(callback.from_user.id)
    result = f"<b>Список ваших заказов ({len(all_orders)}) :</b> \n\n"
    for index, order in enumerate(all_orders):
        result += f"""<b>{index + 1} из {len(all_orders)} </b>
<b>Номер заказа:</b> {order.id}
<b>Вы представились:</b> {order.name}         
<b>Ваш контакт:</b> {order.contact}
<b>Описание заказа:</b> {order.description}
<b>Заказ создан:</b> {order.created_at.strftime("%d.%m.%Y %H:%M")} 
\n"""
    await callback.message.answer(result, reply_markup=get_back_menu())
    await callback.answer()


@router.callback_query(F.data == "remove_order")
async def order_remove(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.del_order)
    await callback.message.answer(
        "Введите <b>номер заказа</b>, который хотите удалить (можно найти в списке заказов):",
        parse_mode=ParseMode.HTML, 
        reply_markup=get_back_menu()
    )
    await callback.answer()


@router.message(OrderStates.del_order)
async def del_user(message: Message, state: FSMContext):
    user_id_text = message.text.strip()

    if not user_id_text.isdigit():
        await message.answer(
            "Это не число. Попробуйте снова:", reply_markup=get_back_menu()
        )
        return
    user_id = int(user_id_text)
    flag = await remove_order(user_id, message.from_user.id)
    if flag == True:
        await message.answer(
            "✅ Данные успешно сохранены!", reply_markup=get_back_menu()
        )
        await state.clear()
    else:
        await message.answer(
            "❌ Нет такого заказа! Попробуйте снова", reply_markup=get_back_menu()
        )
