from aiogram import F, Router
from aiogram.dispatcher import router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.state import StatesGroup, State

from app.database.crud_text import save_text
from app.database.crud_user import is_admin
from app.keyboards.keyboards import edit_keyboard, get_back_menu

router = Router()


class TextStates(StatesGroup):
    waiting_start = State()
    waiting_faq = State()
    waiting_contact = State()


@router.message(Command("panel"))
async def menu_information(message: Message) -> None:
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return
    photo = FSInputFile("img/random.png")
    await message.answer_photo(
        photo=photo,
        reply_markup=edit_keyboard(),
    )


@router.callback_query(F.data == "edit_start")
async def create_order(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id) == False:
        await callback.answer("❗️ У тебя недостаточно прав!")
        return
    await state.set_state(TextStates.waiting_start)
    await callback.message.answer(
        "Пожалуйста, введите текст нового сообщения!:", reply_markup=get_back_menu()
    )
    await callback.answer()


@router.message(TextStates.waiting_start)
async def input_name(message: Message, state: FSMContext):
    await save_text("start", message.text)
    await state.clear()
    await message.answer(
        "Кнопка старта обновлена!",
        reply_markup=get_back_menu(),
    )


@router.callback_query(F.data == "edit_contact")
async def create_order(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id) == False:
        await callback.answer("❗️ У тебя недостаточно прав!")
        return
    await state.set_state(TextStates.waiting_contact)
    await callback.message.answer(
        "Пожалуйста, введите текст нового сообщения!:", reply_markup=get_back_menu()
    )
    await callback.answer()


@router.message(TextStates.waiting_contact)
async def input_name(message: Message, state: FSMContext):
    await save_text("contact", message.text)
    await state.clear()
    await message.answer(
        "Кнопка контаков обновлена!",
        reply_markup=get_back_menu(),
    )


@router.callback_query(F.data == "edit_faq")
async def create_order(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id) == False:
        await callback.answer("❗️ У тебя недостаточно прав!")
        return
    await state.set_state(TextStates.waiting_faq)
    await callback.message.answer(
        "Пожалуйста, введите текст нового сообщения!:", reply_markup=get_back_menu()
    )
    await callback.answer()


@router.message(TextStates.waiting_faq)
async def input_name(message: Message, state: FSMContext):
    await save_text("faq", message.text)
    await state.clear()
    await message.answer(
        "Кнопка старта обновлён!",
        reply_markup=get_back_menu(),
    )
