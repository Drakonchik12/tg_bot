from aiogram import types
from keyboards.main import main_keyboard 
from db import users_collection# Імпортуємо клавіатуру

async def register_user(message: types.Message):
    user_id = message.from_user.id
    nickname = message.text

    if users_collection.find_one({"tg_id": user_id}):
        user = users_collection.find_one({"tg_id": user_id})
        await message.answer(f"Вітаю, {user['nickname']}! Радий, що ви повернулися!", reply_markup=main_keyboard)
        return

    users_collection.insert_one({"tg_id": user_id, "nickname": nickname})
    await message.answer(f"Реєстрація завершена! Ваш нік: {nickname}", reply_markup=main_keyboard)
