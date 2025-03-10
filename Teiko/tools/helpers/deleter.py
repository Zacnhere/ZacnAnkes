import string
import asyncio
import aiofiles
from Teiko import list_admins
from pyrogram import filters
from time import time
from Teiko import *


async def list_admins(client, chat_id):
    admins = []
    async for member in client.get_chat_members(chat_id, filter="administrators"):
        admins.append(member.user.id)
    return admins


async def isGcast(filter, client, update):
    # Membaca daftar kata terlarang dari file
    async with aiofiles.open('bl.txt', mode='r') as file:
        bl_words = {line.strip().lower() async for line in file}

    # Daftar karakter khusus (font aneh) yang harus dihapus
    bl_chars = set("€¥£¢𝑎𝑏𝑐𝑑𝑒𝑓𝑔𝒉𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶..."
                   "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯")  # Truncated for readability

    # Ambil data admin, whitelist, dan blacklist words secara asinkron
    white_list, admins = await asyncio.gather(
        DB.get_list_vars(TB.me.id, f"whitelist_{update.chat.id}") or [],
        list_admins(client, update.chat.id)
    )

    # Jika pengirim adalah admin atau whitelist, biarkan pesan lewat tanpa perubahan
    if update.from_user.id in white_list or update.from_user.id in admins:
        return False

    # Ambil teks pesan
    message_text = update.text.lower()

