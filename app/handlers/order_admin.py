from aiogram import F, Router
from aiogram.dispatcher import router
from aiogram.filters import Command, command
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from app.database.crud_user import is_admin
from app.keyboards.orders_keyboards import (
    complete_orders,
    get_back_orders,
    get_orders_keyboard,
)
from app.database.crud_order import (
    get_admin_orders,
    get_last_order,
    get_old_order,
    remove_admin_order,
    remove_order,
)

router = Router()


@router.message(Command("orders"))
async def order_menu(message: Message):
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return
    photo = FSInputFile("img/work.jpg")
    await message.answer_photo(
        photo=photo,
        reply_markup=get_orders_keyboard(),
    )


@router.callback_query(F.data == "back_orders")
async def order_menu(callback: CallbackQuery):
    photo = FSInputFile("img/work.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption="📋 <b>Меню заказов</b>",
        reply_markup=get_orders_keyboard(),
    )


@router.callback_query(F.data == "orders_admin_list")
async def admin_list(callback: CallbackQuery):
    all_orders = await get_admin_orders()
    result = f"<b>Список заказов ({len(all_orders)}) :</b> \n\n"
    for index, order in enumerate(all_orders):
        result += f"""<b>{index + 1} из {len(all_orders)} </b>
<b>Номер заказа:</b> {order.id}
<b>Имя:</b> {order.name}         
<b>Контакт:</b> {order.contact}
<b>ID:</b> {order.user_id}
<b>Описание заказа:</b> {order.description}
<b>Заказ создан:</b> {order.created_at.strftime("%d.%m.%Y %H:%M")} 
\n"""
    await callback.message.answer(result, reply_markup=get_back_orders())
    await callback.answer()


@router.callback_query(F.data == "old_order")
async def old_order(callback: CallbackQuery):
    order = await get_old_order()
    result = f"""<b>Самый старый заказ:</b> \n
<b>Номер заказа:</b> {order.id}
<b>Имя:</b> {order.name}         
<b>Контакт:</b> {order.contact}
<b>ID:</b> {order.user_id}
<b>Описание заказа:</b> {order.description}
<b>Заказ создан:</b> {order.created_at.strftime("%d.%m.%Y %H:%M")} 
\n"""
    await callback.message.answer(result, reply_markup=get_back_orders())
    await callback.answer()


@router.callback_query(F.data == "last_order")
async def last_order(callback: CallbackQuery):
    order = await get_last_order()
    result = f"""<b>Самый новый заказ:</b> \n
<b>Номер заказа:</b> {order.id}
<b>Имя:</b> {order.name}         
<b>Контакт:</b> {order.contact}
<b>ID:</b> {order.user_id}
<b>Описание заказа:</b> {order.description}
<b>Заказ создан:</b> {order.created_at.strftime("%d.%m.%Y %H:%M")} 
\n"""
    await callback.message.answer(result, reply_markup=get_back_orders())
    await callback.answer()


@router.callback_query(F.data == "сomplete_order")
async def complete_order(callback: CallbackQuery):
    await callback.message.answer(
        "Выберите одно из следующих действий:", reply_markup=complete_orders()
    )
    await callback.answer()


class OrdersNumber(StatesGroup):
    waiting_number = State()


@router.callback_query(F.data == "complete_number")
async def complete_order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrdersNumber.waiting_number)
    await callback.message.answer(
        "Введите номер заказа, который вы выполнили:", reply_markup=get_back_orders()
    )
    await callback.answer()


@router.message(OrdersNumber.waiting_number)
async def complete_order(message: Message, state: FSMContext):
    user_id_text = message.text.strip()

    if not user_id_text.isdigit():
        await message.answer(
            "Это не число. Попробуйте снова:", reply_markup=get_back_orders()
        )
        return
    user_id = int(user_id_text)
    flag = await remove_admin_order(user_id)
    if flag == True:
        await message.answer(
            "✅ Данные успешно сохранены!", reply_markup=get_back_orders()
        )
        await state.clear()
    else:
        await message.answer(
            "❌ Нет такого заказа! Попробуйте снова", reply_markup=get_back_orders()
        )


@router.callback_query(F.data == "complete_first")
async def complete_first(callback: CallbackQuery):
    order = await get_old_order()
    if not order:
        await callback.message.answer(
            "🎉 Похоже вы выполнили все заказы!!!",
        )
        return await callback.answer()
    await remove_admin_order(order.id)
    await callback.message.answer(
        "🌻 Заказ успешно выполнен!", reply_markup=get_back_orders()
    )
    await callback.answer()


@router.callback_query(F.data == "complete_last")
async def complete_last(callback: CallbackQuery):
    order = await get_last_order()
    if not order:
        await callback.message.answer(
            "🎉 Похоже вы выполнили все заказы!!!",
        )
        return await callback.answer()
    await remove_admin_order(order.id)
    await callback.message.answer(
        "🌻 Заказ успешно выполнен!", reply_markup=get_back_orders()
    )
    await callback.answer()
