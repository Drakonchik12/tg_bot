from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Так"), KeyboardButton(text="Ні")],
    ],
    resize_keyboard=True
)