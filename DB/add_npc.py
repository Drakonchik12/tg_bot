from pymongo import MongoClient

def setup_database():
    client = MongoClient("mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")  # Підключення до MongoDB
    db = client["mafia_game"]  # Створення бази даних
    
    
    # Наповнення колекції NPC початковими даними
    db.NPC.insert_many([
            {"name": "Максим", "job": "Інженер", "age": 38, "greeting": "Привіт! Якщо вам потрібен ремонт, звертайтеся."},
            {"name": "Ольга", "job": "Лікар", "age": 40, "greeting": "Доброго дня! Ваше здоров'я — моя турбота."},
            {"name": "Ігор", "job": "Поліцейський", "age": 35, "greeting": "Безпека міста в надійних руках!"},
            {"name": "Катерина", "job": "Художниця", "age": 28, "greeting": "Барви життя — це те, що я люблю створювати!"},
            {"name": "Василь", "job": "Фермер", "age": 50, "greeting": "Свіжі продукти — найкраще, що може бути!"}

    ])
    
    print("NPC успішно додані")

if __name__ == "__main__":
    setup_database()
