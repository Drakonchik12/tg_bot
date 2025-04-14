from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ok_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="OK", callback_data="ok_pressed")]
])