from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Class.NPC import NPC
from aiogram import types
from Class.Users import User
import asyncio
import random
from aiogram.fsm.context import FSMContext
from aiogram import F
from pymongo import MongoClient
from common.keyboards.main import main_keyboard
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from game_message import assign_messages_to_npcs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, types
from modules.newgame.texts import MESSAGES
from common.keyboards.keyboards_common import create_common_keyboard

from common.keyboards.stop import stop_keyboard
from db import users_collection, roles_collection, games_collection

user = None
npcs = []

storage = MemoryStorage()
dp = Dispatcher( storage=storage)

active_votes = {}

async def insert_game_result(user_id: int, role: str, result: bool):

    game_data = {
        "user_id": user_id,
        "difficult": game_difficult,
        "role_id": role,
        "result": result
    }
    
    inserted = await games_collection.insert_one(game_data)
    return inserted.inserted_id

def fill_npcs():
    return NPC.get_random_npcs_4()

def show_npcs(npcs):
    return "\n".join([f"{npc.name}, {npc.job}, {npc.age} років" for npc in npcs])

def assign_roles(user, npcs):
    roles = ["Мирний", "Мирний", "Мафія", "Комісар", "Лікар"]
    random.shuffle(roles)
    # Призначаємо роль користувачу
    # user.role = roles.pop()
    user.role = "Мирний"
    # Призначаємо ролі NPC
    for npc in npcs:
        npc.role = roles.pop()
    return user, npcs

async def first_night_info_for_user(message: types.Message, state: FSMContext, user):
    if not user:
        await message.answer(MESSAGES["role_error"])
        return

    await message.answer(MESSAGES["night_intro"])
    await asyncio.sleep(3)

    role_message = MESSAGES.get(f"intro_{user.role}")
    if role_message:
        await message.answer(role_message)


async def first_night(message: types.Message, state: FSMContext, user, npcs):
    if not user:
        await message.answer(MESSAGES["role_error"])
        return

    role_sequences = {
        "Мафія": [
            MESSAGES["night_commissar"],
            MESSAGES["night_doctor"],
        ],
        "Комісар": [
            MESSAGES["night_mafia"],
            MESSAGES["night_doctor"],
        ],
        "Лікар": [
            MESSAGES["night_mafia"],
            MESSAGES["night_commissar"],
        ],
        "Мирний": [
            MESSAGES["night_mafia"],
            MESSAGES["night_commissar"],
            MESSAGES["night_doctor"],
        ],
    }

    for line in role_sequences.get(user.role, []):
        await asyncio.sleep(3)
        await message.answer(line)

    await asyncio.sleep(3)
    await message.answer(MESSAGES["night_morning"])

    await first_day(message, state, npcs, user)

async def first_day(message: types.Message, state: FSMContext, npcs, user):
    await message.answer(MESSAGES["night_passed_peacefully"])
    
    # Генерація пар NPC та повідомлень
    nickname = user.nickname
    print(nickname)
    npc_message_pairs = assign_messages_to_npcs(npcs, nickname)
    
    # Виведення повідомлень від кожного NPC
    for npc_name, npc_message in npc_message_pairs:
        await asyncio.sleep(3)
        await message.answer(f"{npc_name}: {npc_message}")    

async def first_npc_messages(message: types.Message,state: FSMContext):

    global user, npcs
    
    user_id = message.from_user.id

    await message.answer(MESSAGES["game_exit_hint"], reply_markup=stop_keyboard)
    npcs = fill_npcs()
    user = User.get_user_by_tg_id(user_id)

    if user and npcs:
        user, npcs = assign_roles(user, npcs)
        await message.answer(
            MESSAGES["game_started"].format(role=user.role),
            parse_mode="HTML"
        )
        await asyncio.sleep(3)
        await message.answer(
            MESSAGES["npcs_intro"] + show_npcs(npcs),
            parse_mode="HTML"
        )
    else:
        await message.answer(MESSAGES["load_error"])

    for npc in npcs:
        await asyncio.sleep(3)
        await message.answer(
            MESSAGES["npc_greeting"].format(name=npc.name, greeting=npc.greeting),
            parse_mode="HTML"
        )

    await first_night_info_for_user(message, state, user)
    await asyncio.sleep(5)

def get_info_for_game():
    return user, npcs
    
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
            await night(message, state, user, npcs)
    else:
        await message.answer("⚖️ Голоси розподілилися порівну! Повторне голосування серед кандидатів.")

async def night(message: types.Message, state:FSMContext, user, npcs):
    await asyncio.sleep(3)
    await message.answer("🌙 Ніч настала... Всі мешканці міста засинають.")
    await asyncio.sleep(3)
    role = user.role
   
    if role == "Мафія":
        print("🔴 Ви — Мафія! Ваше завдання — усунути мирних жителів.")
        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")
    elif role == "Мирний":
        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")
        
        doctor_ch = await doctor_choice(user, npcs)
        npcs = await mafia_kill(npcs, user, doctor_ch, message)
        
        if npcs == None:
            
            return
        
        await message.answer("🌅 Наступає ранок. Місто прокидається.")
        
        await first_day(message, state, npcs, user)
        await voting(message, state, user, npcs)
        
    elif role == "Комісар":
        print("🟡 Ви — Комісар! Ви можете перевіряти підозрюваних.")
    elif role == "Лікар":
        print("🟢 Ви — Лікар! Ви можете рятувати людей від мафії.")
    else:
        return "❓ Невідома роль!"   
    
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
        await insert_game_result(user.user_id, user.role, False)
        await message.answer("Повертаємось до головного меню.", reply_markup=main_keyboard)
        return None# Гра для користувача завершена
    else:
        npcs = [npc for npc in npcs if npc != victim]
        await message.answer(f"❌ {victim.name} був вбитий мафією!")
    
    return npcs  # Повертаємо оновлений список

async def doctor_choice(user, npcs):
    # Лікар може вибрати будь-кого серед NPC або користувача
    potential_targets = npcs + [user]
    chosen_target = random.choice(potential_targets)
    
    return chosen_target

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
    keyboard = create_common_keyboard([(npc.name, f"vote_{npc.npc_id}") for npc in npcs])
    
    await message.answer("🔸 За кого ви голосуєте?", reply_markup=keyboard)