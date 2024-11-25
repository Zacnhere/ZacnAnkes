from pyrogram import *

from Teiko import *

from pyrogram import Client, filters
from collections import defaultdict
import logging


# Penyimpanan status spam per pengguna dan status aktif/spam
spam_users = defaultdict(int)  # Menyimpan jumlah pesan yang sama yang dikirim oleh pengguna
user_free = set()  # Set pengguna yang bebas dari penghapusan spam
spam_enabled = True  # Status deteksi spam (aktif/tidak)

# Menambahkan admin ID Anda
ADMIN_ID = 1361379181  # Ganti dengan ID admin grup Anda

# Fungsi untuk mendeteksi spam
@PY.BOT("antispam")
async def antispam(client, message):
    global spam_enabled
    
    if not spam_enabled:
        return  # Tidak memproses pesan jika spam tidak diaktifkan
    
    user_id = message.from_user.id
    message_text = message.text
    
    if user_id not in user_free:  # Hanya proses pesan jika pengguna tidak bebas
        spam_users[user_id] += 1
        if spam_users[user_id] >= 2:  # Deteksi spam jika pesan yang sama dikirim 2 kali atau lebih
            if message.chat.get_member(user_id).status != 'administrator':  # Cek apakah pengguna bukan admin
                await message.delete()  # Hapus pesan spam
                await message.reply('Pesan spam Anda telah dihapus.')
                return
    
    # Reset jumlah pesan jika pesan berbeda
    spam_users[user_id] = 0

# Fungsi untuk perintah /on (aktifkan deteksi spam)
@PY.BOT("spamon")
async def on_handler(client, message):
    global spam_enabled
    spam_enabled = True
    await message.reply('Deteksi spam diaktifkan!')

# Fungsi untuk perintah /off (nonaktifkan deteksi spam)
@PY.BOT("spamoff")
async def off_handler(client, message):
    global spam_enabled
    spam_enabled = False
    await message.reply('Deteksi spam dinonaktifkan!')

# Fungsi untuk perintah /free (bebaskan pengguna dari penghapusan spam)
@PY.BOT("free")
async def free_handler(client, message):
    user_free.add(message.from_user.id)
    await message.reply('Anda sekarang bebas dari penghapusan spam!')

