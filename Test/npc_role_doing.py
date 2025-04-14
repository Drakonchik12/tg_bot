import random
from aiogram import types
import asyncio
from aiogram import Bot, Dispatcher, types, F
from easy_game import first_day
from aiogram.fsm.context import FSMContext
from pymongo import MongoClient
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

active_votes = {}
dp = Dispatcher()

client = MongoClient("mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")  
db = client["mafia_game"]
games_collection = db["Games"] 

async def insert_game_result(user_id: int, role: str, result: bool):
    game_data = {
        "user_id": user_id,
        # "difficult": game_difficult,
        "role_id": role,
        "result": result
    }
    
    inserted = await games_collection.insert_one(game_data)
    return inserted.inserted_id

async def mafia_kill(npcs, user, doctor_choice, message: types.Message):
    mafia_choices = [npc for npc in npcs if npc.role != "Мафія"] + [user]
    victim = random.choice(mafia_choices)  # Мафія вибирає жертву
    
    await message.answer(f"\U0001F5E1️ Мафія вибрала свою жертву...")
    print(victim)
    
    # Перевіряємо, чи лікар врятував жертву
    if victim == doctor_choice:
        await message.answer(f"\U0001FA7A Лікар виконав свою роботу! Ніхто не загинув цієї ночі.")
        return npcs  # Повертаємо список без змін
    
    # Видаляємо жертву зі списку
    if victim == user:
        await message.answer(f"❌ Вас вбили. Ви програли.")
        return None  # Гра для користувача завершена
    else:
        npcs = [npc for npc in npcs if npc != victim]
        await message.answer(f"❌ {victim.name} був вбитий мафією!")
    
    return npcs  # Повертаємо оновлений список

async def doctor_choice(user, npcs):
    # Лікар може вибрати будь-кого серед NPC або користувача
    potential_targets = npcs + [user]
    chosen_target = random.choice(potential_targets)
    
    return chosen_target

async def night(message: types.Message, state:FSMContext, user, npcs):
    await asyncio.sleep(3)
    await message.answer("🌙 Ніч настала... Всі мешканці міста засинають.")
    await asyncio.sleep(3)
    role = user.role
   
    if role == "Мафія":
        print("🔴 Ви — Мафія! Ваше завдання — усунути мирних жителів.")
    elif role == "Мирний":
        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")
        
        doctor_ch = await doctor_choice(user, npcs)
        npcs = await mafia_kill(npcs, user, doctor_ch, message)
        
        await message.answer("🌅 Наступає ранок. Місто прокидається.")
        
        await first_day(message, state, npcs, user)
        await voting(message, state, user, npcs)
        
    elif role == "Комісар":
        print("🟡 Ви — Комісар! Ви можете перевіряти підозрюваних.")
    elif role == "Лікар":
        print("🟢 Ви — Лікар! Ви можете рятувати людей від мафії.")
    else:
        return "❓ Невідома роль!"


# 🔹 Функція запуску голосування
async def voting(message: types.Message, state: FSMContext, user, npcs):
    chat_id = message.chat.id
    votes = {npc.npc_id: 0 for npc in npcs}
    votes[user.user_id] = 0  

    # NPC голосують випадково
    for npc in npcs:
        vote_target = random.choice([npc.npc_id for npc in npcs] + [user.user_id])
        if vote_target == user.user_id:
            name_target = user.nickname
        else:
            name_target = next(npc.name for npc in npcs if npc.npc_id == vote_target)
        print(name_target)
        votes[vote_target] += 1
        # await message.answer(f"{npc.name} голосує за {name_target}")


    # Зберігаємо голосування
    active_votes[chat_id] = {"votes": votes, "npcs": npcs, "user": user}

    # Кнопки для голосування
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=npc.name, callback_data=f"vote_{npc.npc_id}")] for npc in npcs
        ]
    )

    await message.answer("🔸 За кого ви голосуєте?", reply_markup=keyboard)

# 🔹 Обробка голосу користувача
@dp.callback_query(F.data.startswith("vote_"))
async def process_vote(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    user_vote = callback.data.replace("vote_", "")

    if chat_id not in active_votes:
        await callback.message.answer("⚠️ Помилка! Голосування не знайдено.")
        return

    votes = active_votes[chat_id]["votes"]
    npcs = active_votes[chat_id]["npcs"]
    user = active_votes[chat_id]["user"]

    if user_vote in votes:
        votes[user_vote] += 2  # Голос користувача важить більше

    await callback.message.edit_text("✅ Ви проголосували! Обробляємо результати...")

    await handle_voting_results(callback.message, state, user, npcs, votes)

# 🔹 Функція обробки результатів
async def handle_voting_results(message: types.Message,state: FSMContext, user, npcs, votes):
    max_votes = max(votes.values())
    candidates = [npc_id for npc_id, v in votes.items() if v == max_votes]

    if len(candidates) == 1:
        eliminated_id = candidates[0]
        eliminated = next((npc for npc in npcs if str(npc.npc_id) == str(eliminated_id)), None)

        if eliminated and eliminated.npc_id == user.user_id:
            await message.answer("❌ Вас страчено. Ви програли.")
            await insert_game_result(user.user_id, user.role, False)
            return
        else:
            npcs.remove(eliminated)
            await message.answer(f"❌ {eliminated.name} страчено! Його роль була: {eliminated.role}")

            if eliminated.role == "Мафія":
                await message.answer("✅ Ви виграли! Мафія ліквідована.")
                await insert_game_result(user.user_id, user.role, True)
                return
            print(npcs)
            await night(message, user, npcs)
    else:
        await message.answer("⚖️ Голоси розподілилися порівну! Повторне голосування серед кандидатів.")
        
