from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мої дані"), KeyboardButton(text="Допомога")],
        [KeyboardButton(text="Нова гра")]
    ],
    resize_keyboard=True
)
