from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_common_keyboard(items: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=callback)] for text, callback in items
        ]
    )