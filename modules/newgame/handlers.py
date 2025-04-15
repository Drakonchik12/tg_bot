from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types, F, Router
from common.keyboards.difficult import difficulty_keyboard
from common.keyboards.ok import ok_keyboard
from common.keyboards.yes_no import keyboard_yes_no
from modules.newgame.service import handle_voting_results, first_npc_messages, first_night, get_info_for_game, voting
from bot import dp
router = Router()

active_votes = {}

@router.message(F.text == "Нова гра")
async def new_game(message: types.Message):
    await message.answer("Оберіть рівень складності:", reply_markup=difficulty_keyboard)

# 🔹 Обробка голосу користувача
@router.callback_query(F.data.startswith("vote_"))
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

@router.message(F.text == "Легка")
async def easy_game(message: types.Message, state: FSMContext):
    global game_difficult
    game_difficult = "Легка"
    await first_npc_messages(message, state)
    await message.answer("Натисни 'OK' щоб продовжити", reply_markup=ok_keyboard)

@router.callback_query(F.data == "ok_pressed")
async def process_callback_ok(callback_query: CallbackQuery, state: FSMContext):
    print("Кнопка ок")
    user, npcs = get_info_for_game()
    await first_night(callback_query.message, state, user, npcs)
    await callback_query.message.answer("Оберіть чи хочете голосувати за мафію в перший день", reply_markup=keyboard_yes_no)

@router.message(F.text == "Так")
async def easy_game_first_voit_yes(message: types.Message, state: FSMContext):
   print("Так")
   user, npcs = get_info_for_game()
   await voting(message,state, user, npcs)

@router.message(F.text == "Ні")
async def easy_game_first_voit_no(message: types.Message, state: FSMContext):
   print("Ні")