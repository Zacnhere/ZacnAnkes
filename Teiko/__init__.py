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
