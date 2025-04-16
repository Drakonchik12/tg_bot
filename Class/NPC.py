from pymongo import MongoClient
import random
from db import db

class NPC:
    def __init__(self, npc_id, name, job, age, greeting):
        self.npc_id = npc_id
        self.name = name
        self.job = job
        self.age = age
        self.greeting = greeting
        self.role = None  # Поле для ролі, яке буде заповнене пізніше
    
    def __repr__(self):
        return f"NPC({self.name}, {self.job}, {self.age})"

    @staticmethod
    def get_random_npcs_4(db_url="mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0", db_name="mafia_game", collection_name="NPC", count=4):
        # client = MongoClient(db_url)
        # db = client[db_name]
        collection = db[collection_name]
        
        npcs = list(collection.aggregate([{'$sample': {'size': count}}]))
        
        npc_objects = [NPC(npc["_id"], npc["name"], npc["job"], npc["age"], npc["greeting"]) for npc in npcs]
        
        # client.close()
        return npc_objects
    
    # @staticmethod
    # def get_random_npcs_6(db_url="mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0", db_name="mafia_game", collection_name="NPC", count=6):
    #     client = MongoClient(db_url)
    #     db = client[db_name]
    #     collection = db[collection_name]
        
    #     npcs = list(collection.aggregate([{'$sample': {'size': count}}]))
        
    #     npc_objects = [NPC(npc["_id"], npc["name"], npc["job"], npc["age"], npc["greeting"]) for npc in npcs]
        
    #     client.close()
    #     return npc_objects
    
    # @staticmethod
    # def get_random_npcs_8(db_url="mongodb://oopden334:oopden334@cluster0-shard-00-00.lpqnt.mongodb.net:27017,cluster0-shard-00-01.lpqnt.mongodb.net:27017,cluster0-shard-00-02.lpqnt.mongodb.net:27017/?replicaSet=atlas-nidltb-shard-0&ssl=true&authSource=admin&retryWrites=true&w=majority&appName=Cluster0", db_name="mafia_game", collection_name="NPC", count=8):
    #     client = MongoClient(db_url)
    #     db = client[db_name]
    #     collection = db[collection_name]
        
    #     npcs = list(collection.aggregate([{'$sample': {'size': count}}]))
        
    #     npc_objects = [NPC(npc["_id"], npc["name"], npc["job"], npc["age"], npc["greeting"]) for npc in npcs]
        
    #     client.close()
    #     return npc_objects