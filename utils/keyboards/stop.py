from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Завершити")]
    ],
    resize_keyboard=True
)