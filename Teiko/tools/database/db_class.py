import sys

from motor.motor_asyncio import AsyncIOMotorClient
from config import Config



class Database(object):
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URL)
        self.db = self.client["TeikoUbotDB"]

        # mongo db collections
        self.varsdb = self.db.varsdb
        self.activ = self.db.activ


    # ANKES EXPIRED(TIME)
    async def add_exp(self, chat_id, time):
        x = await self.activ.find_one({"_id": chat_id})
        if x:
            await self.activ.update_one(
                {"_id": chat_id},
                {"$set": {"time": time}},
            )
        else:
            await self.activ.insert_one({"_id": chat_id, "time": time})
            
    async def rem_exp(self, chat_id):
        await self.activ.delete_one({"_id": chat_id})
        
    async def get_exp(self, chat_id):
        active = await self.activ.find_one({"_id": chat_id})
        if not active:
            return None
        return active["time"]

    
    # VARS
    async def set_vars(self, user_id, vars_name, value, query="vars"):
        update_data = {"$set": {f"{query}.{vars_name}": value}}
        await self.varsdb.update_one({"_id": user_id}, update_data, upsert=True)

    async def get_vars(self, user_id, vars_name, query="vars"):
        result = await self.varsdb.find_one({"_id": user_id})
        return result.get(query, {}).get(vars_name, None) if result else None

    async def remove_vars(self, user_id, vars_name, query="vars"):
        remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
        await self.varsdb.update_one({"_id": user_id}, remove_data)

    async def all_vars(self, user_id, query="vars"):
        result = await self.varsdb.find_one({"_id": user_id})
        return result.get(query) if result else None

    async def remove_all_vars(self, user_id):
        await self.varsdb.delete_one({"_id": user_id})

    async def get_list_vars(self, user_id, vars_name, query="vars"):
        vars_data = await DB.get_vars(user_id, vars_name, query)
        return [int(x) for x in str(vars_data).split()] if vars_data else []

    async def add_list_vars(self, user_id, vars_name, value, query="vars"):
        vars_list = await DB.get_list_vars(user_id, vars_name, query)
        vars_list.append(value)
        await DB.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

    async def remove_list_vars(self, user_id, vars_name, value, query="vars"):
        vars_list = await DB.get_list_vars(user_id, vars_name, query)
        if value in vars_list:
            vars_list.remove(value)
            await DB.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)


DB = Database()
