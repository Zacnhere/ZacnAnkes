from pyrogram import *

from Teiko import *

from pyrogram import Client, filters
import asyncio
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# Cache untuk menyimpan data sementara
user_cache = {}

@Client.on_message(filters.text)
async def antispam_handler(client: Client, message: Message):
    chat_id = message.chat.id

    # Cek status antispam
    antispam_status = await db.get_vars(client.me.id, f"antispam_chat_{chat_id}")
    if not antispam_status:  # Jika antispam tidak aktif
        return

    user_id = message.from_user.id
    user = await client.get_users(user_id)
    this_user = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    current_time = asyncio.get_event_loop().time()

    # Ambil data pengguna dari cache atau database
    user_data = user_cache.get((user_id, chat_id))
    if not user_data:
        user_data = await db.get_user_data(user_id, chat_id) or {
            "last_message_time": 0,
            "message_count": 0,
        }
        user_cache[(user_id, chat_id)] = user_data

    # Cek jika pengguna mengirim pesan terlalu cepat
    if current_time - user_data["last_message_time"] < 2:
        user_data["message_count"] += 1

        if user_data["message_count"] > 2:
            btn = ikb([["| support - https://t.me/shinchilld |"]])

            await client.send_message(
                chat_id,
                f"{this_user}\n<b>Peringatan! Jangan mengirim pesan terlalu cepat!</b>",
                reply_markup=btn,
            )
            await message.delete()
    else:
        user_data["message_count"] = 0  # Reset hitungan pesan

    user_data["last_message_time"] = current_time
    user_cache[(user_id, chat_id)] = user_data  # Simpan kembali data pengguna


@Client.on_message(filters.command("antispam"))
async def antispam_toggle(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply(
            "<b>Usage:</b>\n/antispam on or off"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()
    if command not in query:
        return await message.reply(
            "<b>Usage:</b>\n/antispam on or off"
        )

    txt = (
        "<b>Antispam activated successfully</b>"
        if command == "on"
        else "<b>Antispam deactivated successfully</b>"
    )
    await db.set_vars(client.me.id, f"antispam_chat_{message.chat.id}", query[command])
    return await message.reply(txt)
    
