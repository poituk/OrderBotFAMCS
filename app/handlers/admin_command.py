from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from app.keyboards.admin_keyboards import admins_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from app.database.crud_user import is_admin, new_admin, get_admins, remove_admin

class AdminStates(StatesGroup):
    user_id = State()
    name = State()
    del_user_id = State()


router = Router()


@router.message(Command("getmyid"))
async def get_my_id(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


@router.message(Command("superuser"))
async def super_user(message: Message):
    user = {
        "name": "admin",
        "user_id": int(message.from_user.id)
    }
    await new_admin(user)
    await message.answer(f"Ты стал админом 🤐!")


@router.message(Command("admin"))
async def admin_menu(message: Message):
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return
    photo = FSInputFile("img/moder.jpg")
    await message.answer_photo(
        photo=photo,
        reply_markup=admins_keyboard(),
    )


@router.callback_query(F.data == "admin_add")
async def admin_add(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.message.answer("❗️ У тебя недостаточно прав!")
        return await callback.answer()
    await state.set_state(AdminStates.user_id)
    await callback.message.answer(
        "Введите <b>ID</b> пользователя (/getmyid - узнать <b>СВОЙ</b> ID )):",
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@router.message(AdminStates.user_id)
async def get_user_id(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return
    
    user_id_text = message.text.strip()

    if not user_id_text.isdigit():
        await message.answer("Это не число. Попробуйте снова:")
        return  
    user_id = int(user_id_text)
    await state.update_data(user_id=user_id)
    await state.set_state(AdminStates.name)
    await message.answer("Введите имя нового администратора!")


@router.message(AdminStates.name)
async def get_name(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return
    
    name = message.text

    if not name:
        await message.answer("Напишите хоть что-нибудь. Попробуйте снова:")
        return

    await state.update_data(name=name)
    data = await state.get_data()
    print(data)
    await new_admin(data)
    await state.clear()
    await message.answer("✅ Данные успешно сохранены!")


@router.callback_query(F.data == "admin_remove")
async def admin_remove(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id) == False:
        await callback.message.answer("❗️ У тебя недостаточно прав!")
        return await callback.answer()

    await state.set_state(AdminStates.del_user_id)
    await callback.message.answer(
        "Введите <b>ID</b> пользователя, которого хотите удалить (можно найти в списке админов)):",
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@router.message(AdminStates.del_user_id)
async def del_user(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id) == False:
        await message.answer("❗️ У тебя недостаточно прав!")
        return 

    user_id_text = message.text.strip()

    if not user_id_text.isdigit():
        await message.answer("Это не число. Попробуйте снова:")
        return
    user_id = int(user_id_text)
    flag = await remove_admin(user_id)
    if flag == True:
        await message.answer("✅ Данные успешно сохранены!")
        await state.clear()
    else:
        await message.answer("❌ Нет такого пользователя! Попробуйте снова")


@router.callback_query(F.data == "admin_list")
async def admin_list(callback: CallbackQuery):
    if await is_admin(callback.from_user.id) == False:
        await callback.message.answer("❗️ У тебя недостаточно прав!")
        return await callback.answer()

    all_admins = await get_admins()
    result = f'<b>Список администраторов ({len(all_admins)}) :</b> \n\n'
    for (index, admin) in enumerate(all_admins):
        result += f'<b>{index + 1} из {len(all_admins)}</b> \n<b>Имя администратора:</b> {admin.name} \n<b>ТГ ID:</b> {admin.user_id}\n\n'  
    await callback.message.answer(result) 
    await callback.answer()
