from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

difficulty_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легка"), KeyboardButton(text="Середня"), KeyboardButton(text="Складна")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)