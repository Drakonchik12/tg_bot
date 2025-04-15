from aiogram import types, Router, F
from common.keyboards.main import main_keyboard
from db import users_collection
from modules.main.service import register_nickname  # імпортуємо функцію реєстрації, якщо вона в іншому файлі

router = Router()

@router.message(F.text == "/start")
async def start_command(message: types.Message):
    user_id = message.from_user.id
   
    user = users_collection.find_one({"tg_id": user_id})
    
    if user:
        await message.answer(f"Вітаю, {user['nickname']}! Радий, що ви повернулися!", reply_markup=main_keyboard)
    else:
        await message.answer("Вітаю! Будь ласка, введіть ваш нікнейм для реєстрації.")
        router.message.register(register_nickname)

@router.message(F.text == "Назад")
async def back_to_main(message: types.Message):
    await message.answer("Повертаємось до головного меню.", reply_markup=main_keyboard)