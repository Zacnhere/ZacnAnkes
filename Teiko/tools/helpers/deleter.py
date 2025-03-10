import string
import asyncio
import aiofiles
from pyrogram.enums import ChatMembersFilter
from pyrogram import filters
from time import time
from Teiko.tools.helpers import deleter
from Teiko import *


def list_admins(chat_id):
    return []


async def get_admins(client, chat_id):
    """Mengambil daftar admin dari grup."""
    admins = []
    try:
        async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            if member.user and member.user.id:
                admins.append(member.user.id)
    except Exception as e:
        print(f"Error mengambil admin: {e}")
    return admins

async def load_blacklist():
    """Membaca daftar blacklist secara asinkron"""
    try:
        async with aiofiles.open("bl.txt", mode="r", encoding="utf-8") as file:
            bl_words = {line.strip().lower() async for line in file if line.strip()}
        return bl_words
    except Exception as e:
        print(f"Error membaca bl.txt: {e}")
        return set()

async def isGcast(client, message):
    """Mengecek apakah pesan melanggar blacklist dan bukan dari admin atau whitelist."""
    chat_id = message.chat.id
    sender_id = message.from_user.id

    # Muat blacklist dari file
    bl_words = await load_blacklist()
    if not bl_words:
        print("Blacklist kosong atau gagal dimuat!")

    # Karakter aneh yang harus dihapus
    bl_chars = set("€¥£¢𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝒉𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶..."
                   "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯")

    # Ambil data admin dan whitelist
    white_list, admins = await asyncio.gather(
        DB.get_list_vars(TB.me.id, f"whitelist_{chat_id}") or [],
        get_admins(client, chat_id)
    )

    # Jika pengirim adalah admin atau whitelist, biarkan pesan lewat
    if sender_id in white_list or sender_id in admins:
        return False

    # Ambil teks pesan dan bersihkan dari karakter aneh
    if not message.text:
        return False  # Abaikan jika bukan pesan teks
    
    message_text = message.text.lower()
    message_text = "".join(c for c in message_text if c not in bl_chars)

    # Cek apakah ada kata yang cocok dalam blacklist
    for word in bl_words:
        if word in message_text:
            print(f"Pesan terdeteksi mengandung kata terlarang: {word}")
            return True  # Pesan terindikasi melanggar blacklist

    return False  # Pesan aman

Ankes = filters.create(isGcast)
