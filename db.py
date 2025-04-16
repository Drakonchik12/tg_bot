import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tls=True,
    tlsCAFile=certifi.where())

db = client["mafia_game"]
users_collection = db["Users"]
games_collection = db["Games"]
roles_collection = db["Roles"]
