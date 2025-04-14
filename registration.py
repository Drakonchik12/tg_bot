from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def register_user(message: types.Message, users_collection):
    user_id = message.from_user.id
    nickname = message.text
    
    if users_collection.find_one({"tg_id": user_id}):
        user = users_collection.find_one({"tg_id": user_id})
        await message.answer(f"Вітаю, {user['nickname']}! Радий, що ви повернулися!", reply_markup=main_keyboard)
        return
    
    users_collection.insert_one({"tg_id": user_id, "nickname": nickname})
    await message.answer(f"Реєстрація завершена! Ваш нік: {nickname}", reply_markup=main_keyboard)

# Кнопки основного меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мої дані"), KeyboardButton(text="Мої ігри")],
        [KeyboardButton(text="Допомога"), KeyboardButton(text="Нова гра")]
    ],
    resize_keyboard=True
)
