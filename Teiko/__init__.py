import uvloop
import asyncio
import logging
import os
from pyrogram import *
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.types import Message
from pyromod import listen
from rich.logging import RichHandler
from config import Config
from dotenv import load_dotenv

# Install uvloop untuk mempercepat asyncio
uvloop.install()

# Memuat variabel lingkungan dari file .env (jika ada)
load_dotenv()

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(RichHandler())

class ConnectionHandler(logging.Handler):
    def emit(self, record):
        error_types = ["OSError", "TimeoutError"]
        if any(error_type in record.getMessage() for error_type in error_types):
            logger.error(f"Critical error detected, restarting bot...")
            os.system(f"kill -9 {os.getpid()} && python3 -m Teiko")

# Custom Bot Class (inherit dari pyrogram.Client)
class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_id = Config.API_ID
        self.api_hash = Config.API_HASH
        self.bot_token = Config.BOT_TOKEN
        
    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func
        return decorator 
    
    async def start(self):
        await super().start()


TB = Bot(name="ZacnBot")

# Modul Database dan Helper (teiko.tools)
from Teiko.tools.database import *
from Teiko.tools.helpers import *
from Teiko.tools.functions import *

# Fungsi untuk mengelola admin
async def list_admins(client, chat_id):
    chat_members = await client.get_chat_members(chat_id)
    return [member.user.id for member in chat_members if member.status in ['administrator', 'creator']]

# Fungsi untuk memeriksa izin bot
async def check_permissions(client, chat_id):
    chat = await client.get_chat(chat_id)
    if not chat.can_delete_messages:
        return False
    return True

# Menangani perintah start
@TB.on_message(filters.private)
async def start(client, message):
    msg = MSG.START(message)
    buttons = BTN.START(message)
    await message.reply(msg, reply_markup=buttons)

# Menangani callback untuk help
@TB.on_callback_query(filters.regex("AH"))
async def help_callback(client, callback_query):
    buttons = ikb([["| back - home |"]])
    await callback_query.edit_message_text(MSG.HELP(callback_query), reply_markup=buttons)

# Menangani callback untuk kembali ke home
@TB.on_callback_query(filters.regex("home"))
async def home_callback(client, callback_query):
    buttons_home = BTN.START(callback_query)
    await callback_query.edit_message_text(MSG.START(callback_query), reply_markup=buttons_home)

# Menangani perintah adduser (untuk menambah pengguna ke daftar Anti-User)
@TB.on_message(filters.group)
@TB.OWNER
async def add_user_to_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if user_id in anti:
            return await message.reply(f"<b>User is already in Anti-User list!</b>")

        await DB.add_list_vars(TB.me.id, "anti_message_user", user.id)
        return await message.reply(f"<b>Added to Anti-User list:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")

    except Exception as e:
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

# Menangani perintah remuser (untuk menghapus pengguna dari daftar Anti-User)
@TB.on_message(filters.group)
@TB.OWNER
async def remove_user_from_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if user_id not in anti:
