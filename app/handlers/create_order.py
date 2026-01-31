from mailbox import Message
from pkgutil import get_data
from aiogram import F, Router
from aiogram.dispatcher import router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


router = Router()


class Form(StatesGroup):
    name = State()
    contact = State()
    description = State()


@router.callback_query(F.data == "order")
async def create_order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback.message.answer("Пожалуйста, введите ваше имя:")
    await callback.answer()


@router.message(Form.name)
async def input_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.contact)
    await message.answer("Отлично! Теперь введите ваш email или телефон!:")


@router.message(Form.contact)
async def input_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(Form.description)
    await message.answer("Настало время кратко описать проект!")


@router.message(Form.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()

    await state.clear()
    await message.answer("✅ Данные успешно сохранены!")
