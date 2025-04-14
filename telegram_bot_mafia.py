import asyncio
import random
from pymongo import MongoClient
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from registration import register_user, main_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from user_data import show_user_data, edit_nickname, edit_nickname_keyboard
from easy_game import first_npc_messages, first_night, get_info_for_game, stop_keyboard, first_day
from Test.npc_role_doing import night

TOKEN = "7816519995:AAFmGKyRikmRqXsYytD9m5ti7GUd2EB1j5s"  # Замініть на свій токен

bot = Bot(token=TOKEN)
dp = Dispatcher()

active_votes = {}

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="OK", callback_data="ok_pressed")]
])

keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Так"), KeyboardButton(text="Ні")],
    ],
    resize_keyboard=True
)


client = MongoClient("mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")  
db = client["mafia_game"]
users_collection = db["Users"]
games_collection = db["Games"] 



async def insert_game_result(user_id: int, role: str, result: bool):

    game_data = {
        "user_id": user_id,
        "difficult": game_difficult,
        "role_id": role,
        "result": result
    }
    
    inserted = await games_collection.insert_one(game_data)
    return inserted.inserted_id


@dp.callback_query(F.data == "ok_pressed")
async def process_callback_ok(callback_query: CallbackQuery, state: FSMContext):
    print("Кнопка ок")
    user, npcs = get_info_for_game()
    await first_night(callback_query.message, state, user, npcs)
    await callback_query.message.answer("Оберіть чи хочете голосувати за мафію в перший день", reply_markup=keyboard_yes_no)
    

    

@dp.message(F.text == "Так")
async def easy_game_first_voit_yes(message: types.Message, state: FSMContext):
   print("Так")
   user, npcs = get_info_for_game()
   await voting(message,state, user, npcs)

@dp.message(F.text == "Ні")
async def easy_game_first_voit_no(message: types.Message, state: FSMContext):
   print("Ні")

@dp.message(F.text == "Мої дані")
async def my_data(message: types.Message):
    await show_user_data(message, users_collection, games_collection)

async def main():
    await dp.start_polling(bot)
# Панель для вибору рівня складності
difficulty_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легка"), KeyboardButton(text="Середня"), KeyboardButton(text="Складна")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

# Обробник команди /start
@dp.message(F.text == "/start")
async def start_command(message: types.Message):
    user_id = message.from_user.id
   
    user = users_collection.find_one({"tg_id": user_id})
    
    if user:
        await message.answer(f"Вітаю, {user['nickname']}! Радий, що ви повернулися!", reply_markup=main_keyboard)
    else:
        await message.answer("Вітаю! Будь ласка, введіть ваш нікнейм для реєстрації.")
        dp.message.register(register_nickname)

# Очікуємо введення нікнейму
async def register_nickname(message: types.Message):
    await register_user(message, users_collection)

@dp.message(F.text == "Редагувати нікнейм")
async def request_new_nickname(message: types.Message):
    await message.answer("Введіть новий нікнейм:")
    dp.message.register(update_nickname)

async def update_nickname(message: types.Message):
    await edit_nickname(message, users_collection)


@dp.message(F.text == "Легка")
async def easy_game(message: types.Message, state: FSMContext):
    global game_difficult
    game_difficult = "Легка"
    await first_npc_messages(message, state)
    await message.answer("Натисни 'OK' щоб продовжити", reply_markup=keyboard)


@dp.message(F.text == "Назад")
async def back_to_main(message: types.Message):
    await message.answer("Повертаємось до головного меню.", reply_markup=main_keyboard)

@dp.message(F.text == "Нова гра")
async def new_game(message: types.Message):
    await message.answer("Оберіть рівень складності:", reply_markup=difficulty_keyboard)



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
            await night(message, state, user, npcs)
    else:
        await message.answer("⚖️ Голоси розподілилися порівну! Повторне голосування серед кандидатів.")
        

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

    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
