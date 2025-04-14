from pymongo import MongoClient
client = MongoClient("mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")  
db = client["mafia_game"]
games_collection = db["Games"]

def insert_game_result(user_id: int, role: str, result: bool):
    
    game_data = {
        "user_id": user_id,
        "difficult":"Легка",
        "role_id": role,
        "result": result
    }
    
    inserted = games_collection.insert_one(game_data)
    return inserted.inserted_id

user_id = "67dc31a10bf73485a72f74b1"
role = "Мафія"
result = True
insert_game_result(user_id, role, result)