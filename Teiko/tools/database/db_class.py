import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config


class Database(object):
    def __init__(self):
        # Membuat koneksi ke MongoDB menggunakan URL dari konfigurasi
        self.client = AsyncIOMotorClient(Config.MONGO_URL)
        self.db = self.client["TeikoUbotDB"]

        # Koleksi untuk menyimpan variabel dan status aktivitas
        self.varsdb = self.db.varsdb
        self.activ = self.db.activ

    # ANKES EXPIRED (TIME)
    async def add_exp(self, chat_id, time):
        try:
            # Mengecek apakah chat_id sudah ada
            x = await self.activ.find_one({"_id": chat_id})
            if x:
                # Update waktu jika sudah ada
                await self.activ.update_one(
                    {"_id": chat_id},
                    {"$set": {"time": time}},
                )
            else:
                # Insert data baru jika belum ada
                await self.activ.insert_one({"_id": chat_id, "time": time})
        except Exception as e:
            print(f"Error adding expiration for chat {chat_id}: {e}")

    async def rem_exp(self, chat_id):
        try:
            # Menghapus waktu kadaluwarsa untuk chat_id
            await self.activ.delete_one({"_id": chat_id})
        except Exception as e:
            print(f"Error removing expiration for chat {chat_id}: {e}")

    async def get_exp(self, chat_id):
        try:
            # Mengambil waktu kadaluwarsa untuk chat_id
            active = await self.activ.find_one({"_id": chat_id})
            return active["time"] if active else None
        except Exception as e:
            print(f"Error retrieving expiration for chat {chat_id}: {e}")
            return None

    # VARS (User Variables)
    async def set_vars(self, user_id, vars_name, value, query="vars"):
        try:
            # Menyimpan atau memperbarui variabel untuk pengguna tertentu
            update_data = {"$set": {f"{query}.{vars_name}": value}}
            await self.varsdb.update_one({"_id": user_id}, update_data, upsert=True)
        except Exception as e:
            print(f"Error setting variable for user {user_id}: {e}")

    async def get_vars(self, user_id, vars_name, query="vars"):
        try:
            # Mengambil nilai variabel berdasarkan user_id dan vars_name
            result = await self.varsdb.find_one({"_id": user_id})
            return result.get(query, {}).get(vars_name, None) if result else None
        except Exception as e:
            print(f"Error retrieving variable for user {user_id}: {e}")
            return None

    async def remove_vars(self, user_id, vars_name, query="vars"):
        try:
            # Menghapus variabel untuk pengguna dari koleksi
            remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
            await self.varsdb.update_one({"_id": user_id}, remove_data)
        except Exception as e:
            print(f"Error removing variable for user {user_id}: {e}")

    async def all_vars(self, user_id, query="vars"):
        try:
            # Mengambil semua variabel yang terkait dengan user_id
            result = await self.varsdb.find_one({"_id": user_id})
            return result.get(query) if result else None
        except Exception as e:
            print(f"Error retrieving all variables for user {user_id}: {e}")
            return None

    async def remove_all_vars(self, user_id):
        try:
            # Menghapus semua variabel untuk user_id dari koleksi
            await self.varsdb.delete_one({"_id": user_id})
        except Exception as e:
            print(f"Error removing all variables for user {user_id}: {e}")

    async def get_list_vars(self, user_id, vars_name, query="vars"):
        try:
            # Mengambil data list variabel dan mengonversinya menjadi integer
            vars_data = await self.get_vars(user_id, vars_name, query)
            return [int(x) for x in str(vars_data).split()] if vars_data else []
        except Exception as e:
            print(f"Error retrieving list variable for user {user_id}: {e}")
            return []

    async def add_list_vars(self, user_id, vars_name, value, query="vars"):
        try:
            # Menambahkan nilai ke dalam daftar variabel
            vars_list = await self.get_list_vars(user_id, vars_name, query)
            vars_list.append(value)
            await self.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)
        except Exception as e:
            print(f"Error adding to list variable for user {user_id}: {e}")

    async def remove_list_vars(self, user_id, vars_name, value, query="vars"):
        try:
            # Menghapus nilai tertentu dari daftar variabel
            vars_list = await self.get_list_vars(user_id, vars_name, query)
            if value in vars_list:
                vars_list.remove(value)
                await self.set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)
        except Exception as e:
            print(f"Error removing from list variable for user {user_id}: {e}")


# Membuat instance database
DB = Database()

# Fungsi untuk memeriksa status koneksi ke database MongoDB
async def check_db_connection():
    try:
        # Mengecek apakah koneksi ke database berhasil
        await DB.client.admin.command('ping')
        print("MongoDB is connected.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


# Fungsi utama yang dijalankan saat bot dimulai
async def start_bot():
    await check_db_connection()
    # Inisialisasi atau proses lainnya yang diperlukan untuk bot
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(start_bot())
