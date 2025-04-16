from aiogram import types
from common.keyboards.main import main_keyboard
from common.keyboards.edit_nickname import edit_nickname_keyboard
from db import users_collection, games_collection

def count_documents_by_user_id(user_id):
    query = {"user_id": user_id}
    
    count = games_collection.count_documents(query)
    return count

async def show_user_data(message: types.Message):
    user_id = message.chat.id
    print(user_id)
    game_count = count_documents_by_user_id(user_id)
    user = users_collection.find_one({"tg_id": user_id})

    if user:
        await message.answer(
            f"🆔 Ваш ID: {user_id}\n"
            f"👤 Ваш нікнейм: {user['nickname']}\n"
            f"🎮 Кількість зіграних ігор: {game_count}",
            reply_markup=edit_nickname_keyboard
        )
    else:
        await message.answer("Вас не знайдено у базі. Будь ласка, зареєструйтесь, натиснувши /start.")

async def edit_nickname(message: types.Message):
    user_id = message.from_user.id
    new_nickname = message.text

    users_collection.update_one({"tg_id": user_id}, {"$set": {"nickname": new_nickname}})
    await message.answer(f"✅ Ваш нікнейм оновлено: {new_nickname}", reply_markup=main_keyboard)
