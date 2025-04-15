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


from keyboards.stop import stop_keyboard
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
        await message.answer("Не вдалося отримати вашу роль. Гра зупиняється.")
        return

    await message.answer("🌙 Перша ніч настала... Всі мешканці міста засинають.")
    await asyncio.sleep(3)

    if user.role == "Мафія":
        await message.answer(
            "🔪 Ви - мафія!\nВаше завдання: вбити всіх персонажів і залишитися останнім."
        )

    if user.role == "Комісар":
        await message.answer(
            "🕵️ Ви - комісар!\nВаше завдання: дізнатися, хто є мафією, і допомогти мирним перемогти.")

    if user.role == "Лікар":
        await message.answer(
            "🕵️ Ви - лікар!\nВаше завдання: лікувати мирних жителів, допомогти їм вижити."
        )

    if user.role == "Мирний":
        await message.answer(
            "🕵️ Ви - мирний!\nВаше завдання: вижити та правильно визначити мафію щоб вигнати її."
        )


async def first_night(message: types.Message, state: FSMContext, user, npcs):

    if not user:
        await message.answer("Не вдалося отримати вашу роль. Гра зупиняється.")
        return

    if user.role == "Мафія":

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")

        await asyncio.sleep(3)
        await message.answer("🌅 Наступає ранок. Місто прокидається.")# Очікуємо натискання "Ок"

    if user.role == "Комісар":
        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")

        await asyncio.sleep(3)
        await message.answer("🌅 Наступає ранок. Місто прокидається.")

    if user.role == "Лікар":

        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🌅 Наступає ранок. Місто прокидається.")

    if user.role == "Мирний":
        await asyncio.sleep(3)
        await message.answer("🔪 Мафія у пошуках жертви...")

        await asyncio.sleep(3)
        await message.answer("🕵️‍♂️ Комісар виходить на перевірку міста...")

        await asyncio.sleep(3)
        await message.answer("🏥 Лікар оглядає мешканців, шукаючи поранених...")

        await asyncio.sleep(3)
        
        await message.answer("🌅 Наступає ранок. Місто прокидається.")
    
    await first_day(message, state, npcs, user)

async def first_day(message: types.Message, state: FSMContext, npcs, user):
    await message.answer("Ніч пройшла спокійно, але можливо хтось щось бачив чи чув?")
    
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

    await message.answer("Якщо ви захочете вийти з гри, натисніть Завершити, але вам буде зараховано програш", reply_markup=stop_keyboard)
    npcs = fill_npcs()
    user = User.get_user_by_tg_id(user_id)


    if user and npcs:
        user, npcs = assign_roles(user, npcs)
        await message.answer(f"<b>Гра розпочата</b> \nРежим - Легкий\nВаша роль: {user.role}", parse_mode="HTML")
        await asyncio.sleep(3)
        await message.answer("<b>Ваші персонажі:</b>\n" + show_npcs(npcs), parse_mode="HTML")
    else:
        await message.answer("Не вдалося отримати користувача або NPC.")
    for npc in npcs:
        await asyncio.sleep(3)
        await message.answer(f"<b>{npc.name}</b>: {npc.greeting}", parse_mode="HTML")

    await first_night_info_for_user(message, state, user)

    await asyncio.sleep(5)

def get_info_for_game():
    return user, npcs
    


