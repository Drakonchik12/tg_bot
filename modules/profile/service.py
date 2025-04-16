from aiogram import types
from common.keyboards.main import main_keyboard
from common.keyboards.edit_nickname import edit_nickname_keyboard
from db import users_collection, games_collection

def count_documents_by_user_id(user_id):
    query = {"user_id": user_id}
    count = games_collection.count_documents(query)
    return count


def count_wins_by_user_id(user_id):
    query = {"user_id": user_id, "result": True}
    return games_collection.count_documents(query)

def count_losses_by_user_id(user_id):
    query = {"user_id": user_id, "result": False}
    return games_collection.count_documents(query)

async def show_user_data(message: types.Message):
    user_id = message.chat.id
    win_count = count_wins_by_user_id(user_id)
    loss_count = count_losses_by_user_id(user_id)

    game_count = count_documents_by_user_id(user_id)
    user = users_collection.find_one({"tg_id": user_id})

    if user:
        await message.answer(
            f"🆔 Ваш ID: {user_id}\n"
            f"👤 Ваш нікнейм: {user['nickname']}\n"
            f"🎮 Всього ігор: {game_count}\n"
            f"✅ Перемог: {win_count}\n"
            f"❌ Поразок: {loss_count}",
            reply_markup=edit_nickname_keyboard
        )
    else:
        await message.answer("Вас не знайдено у базі. Будь ласка, зареєструйтесь, натиснувши /start.")

async def edit_nickname(message: types.Message):
    user_id = message.from_user.id
    new_nickname = message.text

    users_collection.update_one({"tg_id": user_id}, {"$set": {"nickname": new_nickname}})
    await message.answer(f"✅ Ваш нікнейм оновлено: {new_nickname}", reply_markup=main_keyboard)
