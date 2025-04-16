from aiogram import types, Router, F
from modules.support.service import help


router = Router()

@router.message(F.text == "Допомога")
async def request_new_nickname(message: types.Message):
    await message.answer(help())