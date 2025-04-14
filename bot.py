
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

bot = Bot(token=TOKEN)
dp = Dispatcher()