from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types, F, Router
from common.keyboards.difficult import difficulty_keyboard
from common.keyboards.ok import ok_keyboard
from common.keyboards.yes_no import keyboard_yes_no
from common.keyboards.stop import stop_keyboard
from modules.newgame.service import handle_voting_results, first_npc_messages, first_night, get_info_for_game, voting, active_votes, handle_mafia_results, get_info_for_game, night, active_votes_mafia, active_votes_commissioner, handle_user_commissioner_info_results, active_votes_doctor, handle_user_user_doctor_results
from bot import dp
router = Router()


@router.message(F.text == "Нова гра")
async def new_game(message: types.Message):
    await message.answer("Оберіть рівень складності:", reply_markup=difficulty_keyboard)

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
    
@router.callback_query(F.data.startswith("mafia_kill_"))
async def mafia_vote(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    mafia_vote = callback.data.replace("mafia_kill_", "")
    
    if chat_id not in active_votes_mafia:
        await callback.message.answer("⚠️ Помилка! Вибір мафії не знайдено")
        return
    
    npcs = active_votes_mafia[chat_id]["npcs"]
    user = active_votes_mafia[chat_id]["user"]
    
    await callback.message.edit_text("✅ Ви обрали! Обробляємо результати...")
    await handle_mafia_results(callback.message, state, user, npcs, mafia_vote)
    
 
@router.callback_query(F.data.startswith("commissioner_vote_"))
async def mafia_vote(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    commissioner_vote = callback.data.replace("commissioner_vote_", "")
    
    if chat_id not in active_votes_mafia:
        await callback.message.answer("⚠️ Помилка! Вибір комісара не знайдено")
        return
    
    npcs = active_votes_commissioner[chat_id]["npcs"]
    user = active_votes_commissioner[chat_id]["user"]
    
    await callback.message.edit_text("✅ Ви обрали! Обробляємо результати...")
    await handle_user_commissioner_info_results(callback.message, state, user, npcs, commissioner_vote)
    
@router.callback_query(F.data.startswith("doctor_vote_"))
async def mafia_vote(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    doctor_vote = callback.data.replace("doctor_vote_", "")
    
    if chat_id not in active_votes_doctor:
        await callback.message.answer("⚠️ Помилка! Вибір доктора не знайдено")
        return
    
    npcs = active_votes_doctor[chat_id]["npcs"]
    user = active_votes_doctor[chat_id]["user"]
    
    await callback.message.edit_text("✅ Ви обрали! Обробляємо результати...")
    await handle_user_user_doctor_results(callback.message, state, user, npcs, doctor_vote)


@router.message(F.text == "Легка")
async def easy_game(message: types.Message, state: FSMContext):
    global game_difficult
    game_difficult = "Легка"
    await first_npc_messages(message, state, game_difficult)
    await message.answer("Натисни 'OK' щоб продовжити", reply_markup=ok_keyboard)
    
@router.message(F.text == "Середня")
async def easy_game(message: types.Message, state: FSMContext):
    global game_difficult
    game_difficult = "Середня"
    await first_npc_messages(message, state, game_difficult)
    await message.answer("Натисни 'OK' щоб продовжити", reply_markup=ok_keyboard)
    
@router.message(F.text == "Складна")
async def easy_game(message: types.Message, state: FSMContext):
    global game_difficult
    game_difficult = "Складна"
    await first_npc_messages(message, state, game_difficult)
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
   await message.answer("Нагадуємо ви можете завершити гру в будь який момент", reply_markup=stop_keyboard)
   await voting(message,state, user, npcs)

@router.message(F.text == "Ні")
async def easy_game_first_voit_no(message: types.Message, state: FSMContext):
   print("Ні")
   user, npcs = get_info_for_game()
   await message.answer("Нагадуємо ви можете завершити гру в будь який момент", reply_markup=stop_keyboard)
   chat_id = message.chat.id
   active_votes_mafia[chat_id] = {"npcs": npcs, "user": user}
   await night(message, state, user, npcs)

