from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Class.NPC import NPC
from aiogram import types
from Class.Users import User
import asyncio
import random
from aiogram.fsm.context import FSMContext
from aiogram import F
from pymongo import MongoClient
from handlers.user_data import main_keyboard
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from game_message import assign_messages_to_npcs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, types
from texts import MESSAGES


from utils.keyboards.stop import stop_keyboard
from db import users_collection, roles_collection, games_collection

user = None
npcs = []

storage = MemoryStorage()
dp = Dispatcher( storage=storage)




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
    


