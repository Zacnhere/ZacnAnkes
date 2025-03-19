import string
from pyrogram import filters, enums
from time import time

from Teiko import *

admins_in_chat = {}

async def list_admins(client, chat_id: int):
    """Mengambil daftar admin di grup dan menyimpannya dengan timestamp."""
    global admins_in_chat
    
    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": {
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        },
    }
    return admins_in_chat[chat_id]["data"]

async def is_admin(client, user_id: int, chat_id: int):
    """Mengecek apakah pengguna adalah admin."""
    if chat_id not in admins_in_chat or time() - admins_in_chat[chat_id]["last_updated_at"] > 300:
        await list_admins(client, chat_id)  # Perbarui daftar admin setiap 5 menit
    return user_id in admins_in_chat[chat_id]["data"]

async def isGcast(filter, client, update):
    """Filter untuk mendeteksi pesan blacklist"""
    # Ambil daftar kata blacklist dari file bl.txt
    with open('bl.txt') as file:
        blc_words = {w.lower().strip() for w in file.readlines()}

    # Tambahkan karakter terlarang
    bl_chars = set("$_&-+*"':;!?~`•√π÷×§∆£¢€¥°=%©®™✓<>⟩»≥›«≤‹⟨‰℅∞≠≈←↑↓→¶ΠΩμ♪№₹₱—–·±★†‡¿‽")

    # Gabungkan blacklist kata dan karakter ke dalam satu set
    blc_set = blc_words | bl_chars

    # Ambil daftar whitelist
    white_list = await DB.get_list_vars(TB.me.id, f"whitelist_{update.chat.id}") or set()
    if update.from_user.id in white_list:
        return False  # Abaikan jika user ada di whitelist

    # Pastikan admin tidak terkena filter
    if await is_admin(client, update.from_user.id, update.chat.id):
        return False

    # Ambil blacklist kata dari database
    db_bl_words = await DB.get_vars(TB.me.id, f"word_{update.chat.id}") or set()

    # Gabungkan blacklist dari database dengan blc_set
    full_blacklist = blc_set | set(db_bl_words)

    # Pisahkan teks menjadi kata-kata
    words = set(update.text.lower().split())

    # Cek apakah ada kata yang termasuk dalam blacklist
    if words & full_blacklist:
        return True

    return False

# Buat filter Pyrogram
Ankes = filters.create(isGcast)
    
