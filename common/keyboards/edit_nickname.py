from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

edit_nickname_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Редагувати нікнейм")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)


