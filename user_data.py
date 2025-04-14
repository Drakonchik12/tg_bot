from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def show_user_data(message: types.Message, users_collection, games_collection):
    """Відображає дані користувача: нікнейм, ID та кількість зіграних ігор."""
    user_id = message.from_user.id
    user = users_collection.find_one({"tg_id": user_id})

    if user:
        game_count = games_collection.count_documents({"user_id": user_id})
        await message.answer(
            f"🆔 Ваш ID: {user_id}\n"
            f"👤 Ваш нікнейм: {user['nickname']}\n"
            f"🎮 Кількість зіграних ігор: {game_count}",
            reply_markup=edit_nickname_keyboard
        )
    else:
        await message.answer("Вас не знайдено у базі. Будь ласка, зареєструйтесь, натиснувши /start.")

async def edit_nickname(message: types.Message, users_collection):
    """Очікує новий нікнейм від користувача."""
    user_id = message.from_user.id
    new_nickname = message.text

    users_collection.update_one({"tg_id": user_id}, {"$set": {"nickname": new_nickname}})
    await message.answer(f"✅ Ваш нікнейм оновлено: {new_nickname}", reply_markup=main_keyboard)

# Основна клавіатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мої дані"), KeyboardButton(text="Мої ігри")],
        [KeyboardButton(text="Допомога"), KeyboardButton(text="Нова гра")]
    ],
    resize_keyboard=True
)

# Клавіатура для редагування ніку
edit_nickname_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Редагувати нікнейм")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)



