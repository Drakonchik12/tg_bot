from aiogram import types, Router, F
from modules.profile.service import edit_nickname, show_user_data

router = Router()

    
@router.message(F.text == "Редагувати нікнейм")
async def request_new_nickname(message: types.Message):
    await message.answer("Введіть новий нікнейм:")
    router.message.register(edit_nickname)

@router.message(F.text == "Мої дані")
async def my_data(message: types.Message):
    await show_user_data(message)