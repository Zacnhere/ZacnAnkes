from pyrogram import *

from Teiko import *

import asyncio  # Untuk penjadwalan tugas async
from pyrogram import Client, filters  # Untuk interaksi dengan Telegram melalui Pyrogram
from pyrogram.types import Message  # Tipe pesan Telegram
from pyrogram.errors import FloodWait  # Untuk menangani pembatasan Telegram
from typing import Dict, Tuple  # Untuk tipe anotasi pada fungsi
from pyrogram.types import InlineKeyboardMarkup as ikb  # Untuk membuat tombol inline


user_cache = {}

@PY.UBOT("antispam")
async def _(client, message):
    chat_id = message.chat.id

    antispam_status = await db.get_vars(client.me.id, f"antispam_chat_{chat_id}")
    if not antispam_status or antispam_status != "on":
        return  # Jika antispam tidak aktif, keluar dari fungsi

    user_id = message.from_user.id
    user = await bot.get_users(user_id)
    this_user = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    current_time = asyncio.get_event_loop().time()

    user_data = user_cache.get((user_id, chat_id))
    if not user_data:
        user_data = await db.get_user_data(user_id, chat_id) or {
            "last_message_time": 0,
            "message_count": 0,
        }
        user_cache[(user_id, chat_id)] = user_data

    if current_time - user_data["last_message_time"] < 2:
        user_data["message_count"] += 1

        if user_data["message_count"] > 2:
            btn = ikb([["| support - https://t.me/shinchilld |"]])

            await bot.send_message(
                chat_id,
                f"{this_user}\n<b>Peringatan! Jangan mengirim pesan terlalu cepat!</b>",
                reply_markup=btn,
            )

            await message.delete()

@PY.UBOT("setantispam")
async def _(client, message):
    # Hanya admin yang bisa mengatur antispam
    if not message.chat.admin_rights:
        return await message.reply("<b>Hanya admin yang dapat mengubah pengaturan antispam!</b>")

    # Ambil argumen (on/off)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("<b>Gunakan perintah:</b> <code>setantispam [on/off]</code>")

    status = args[1].lower()
    if status not in ["on", "off"]:
        return await message.reply("<b>Status hanya bisa diatur menjadi:</b> <code>on</code> atau <code>off</code>")

    # Simpan status ke database
    await db.set_vars(client.me.id, f"antispam_chat_{message.chat.id}", status)
    await message.reply(f"<b>Antispam berhasil diatur menjadi:</b> <code>{status}</code>")
    

            user_data["message_count"] = 0
            user_cache[(user_id, chat_id)] = user_data
            return
    else:
        user_data["message_count"] = 1

    user_data["last_message_time"] = current_time
    user_cache[(user_id, chat_id)] = user_data

    if user_data["message_count"] == 1:
        await db.update_user_data(user_id, chat_id, user_data)
