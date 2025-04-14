from pymongo import MongoClient

def setup_database():
    client = MongoClient("mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")  # Підключення до MongoDB
    db = client["mafia_game"]  # Створення бази даних
    
    # Створення колекцій
    db.create_collection("NPC")
    db.create_collection("GameMessages")
    db.create_collection("Roles")
    db.create_collection("Users")
    db.create_collection("Games")
    
    # Наповнення колекції NPC початковими даними
    db.NPC.insert_many([
        {"name": "Джон", "job": "Бізнесмен", "age": 45, "greeting": "Ласкаво просимо до нашого міста!"},
        {"name": "Анна", "job": "Вчитель", "age": 32, "greeting": "Приємно познайомитися, я Анна!"},
    ])
    
    # Наповнення колекції Roles початковими даними
    db.Roles.insert_many([
        {"name": "Мафія"},
        {"name": "Мирний житель"},
        {"name": "Комісар"},
        {"name": "Лікар"}
    ])
    
    # Наповнення колекції GameMessages початковими даними
    db.GameMessages.insert_many([
        {"text": "Настала ніч, всі засинають...", "role_id": None},
        {"text": "Мафія вибирає свою жертву...", "role_id": "Мафія"},
        {"text": "Комісар перевіряє гравця...", "role_id": "Комісар"},
        {"text": "Лікар обирає, кого лікувати...", "role_id": "Лікар"},
        {"text": "Настав день, всі прокидаються...", "role_id": None}
    ])
    
    # Наповнення колекції Users початковими даними
    db.Users.insert_many([
        {"tg_id": 12345, "nickname": "Гравець1"},
        {"tg_id": 67890, "nickname": "Гравець2"}
    ])
    
    # Наповнення колекції Games початковими даними
    db.Games.insert_many([
        {"user_id": 12345, "role_id": "Мафія", "result": True},
        {"user_id": 67890, "role_id": "Мирний житель", "result": False}
    ])
    
    print("База даних і колекції успішно створені та ініціалізовані!")

if __name__ == "__main__":
    setup_database()
