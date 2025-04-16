from pymongo import MongoClient
from db import db

class User:
    def __init__(self, user_id, tg_id, nickname):
        self.user_id = user_id
        self.tg_id = tg_id
        self.nickname = nickname
        self.role = None  # Поле для ролі, яке буде заповнене пізніше
    
    def __repr__(self):
        return f"User({self.nickname}, TG ID={self.tg_id}, Role={self.role})"
    
    @staticmethod
    def get_user_by_tg_id(tg_id, db_url="mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0", db_name="mafia_game", collection_name="Users"):
        # client = MongoClient(db_url)
        # db = client[db_name]
        collection = db[collection_name]
        
        user_data = collection.find_one({"tg_id": tg_id})
        
        # client.close()
        
        if user_data:
            return User(user_data["_id"], user_data["tg_id"], user_data["nickname"])
        else:
            return None
