from pyrogram import *

from Teiko import *

from pyrogram import Client, filters
import asyncio
from pyrogram.types import Message
from pyrogram.errors import FloodWait

import time
from collections import deque

# Simpan pesan yang dikirim dalam rentang waktu tertentu untuk deteksi spam
message_cache = deque()

# Cooldown untuk deteksi spam
SPAM_COOLDOWN = 1  # Deteksi spam 1 detik
MAX_SPAM_COUNT = 2  # 2 pesan dalam 1 detik dianggap spam

# Status Anti-Spam (default aktif)
anti_spam_enabled = True

@PY.BOT("antispam", filters.group)
async def anti_spam(client, message):
    global anti_spam_enabled  # Mengakses variabel status dari luar fungsi

    # Perintah untuk menyalakan atau mematikan anti-spam
    if message.text.lower() == "/antispam on":
        anti_spam_enabled = True
        return await message.reply("<b>Anti-Spam has been enabled.</b>")

    if message.text.lower() == "/antispam off":
        anti_spam_enabled = False
        return await message.reply("<b>Anti-Spam has been disabled.</b>")

    # Jika fitur anti-spam dimatikan, tidak ada yang dilakukan
    if not anti_spam_enabled:
        return

    # Mendapatkan ID pengirim pesan
    user_id = message.from_user.id
    
    # Waktu saat pesan diterima
    current_time = time.time()

    # Menyimpan pesan yang baru diterima dengan waktu saat diterima
    message_cache.append((user_id, message.text, current_time))
    
    # Hapus pesan yang lebih lama dari waktu cooldown
    while message_cache and message_cache[0][2] < current_time - SPAM_COOLDOWN:
        message_cache.popleft()

    # Deteksi spam jika ada dua pesan dari user yang sama dalam 1 detik
    recent_messages = [msg for msg in message_cache if msg[0] == user_id]

    if len(recent_messages) >= MAX_SPAM_COUNT:
        # Jika terdeteksi spam, hapus pesan terakhir
        try:
            await message.delete()
            return await message.reply("<b>Spam detected! Your last message has been deleted as a punishment.</b>")
        except Exception as e:
            return await message.reply(f"<b>Failed to delete message:</b> <code>{str(e)}</code>")
    
    # Informasikan user jika mereka hampir mencapai batas spam
    remaining_spam = MAX_SPAM_COUNT - len(recent_messages)
    if remaining_spam == 1:
        await message.reply("<b>Warning:</b> Please avoid sending the same message multiple times in quick succession.")
    
