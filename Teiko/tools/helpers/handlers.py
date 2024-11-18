from pyrogram import *
from pyrogram.enums import *
from functools import wraps

from Teiko import *
from .deleter import list_admins


async def anti_chat_user(_, client, message):
    chat_ids = await DB.get_list_vars(TB.me.id, "anti_message_user")
    is_user = message.from_user if message.from_user else message.sender_chat
    return is_user.id in chat_ids


class PY:
    @staticmethod
    def BOT(command, additional_filters=None):
        def wrapper(func):
            filters_combined = filters.command(command)
            if additional_filters:
                filters_combined &= additional_filters

            @TB.on_message(filters_combined)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def INLINE(command):
        def wrapper(func):
            @TB.on_inline_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @TB.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def OWNER(func):
        async def function(client, message):
            user = message.from_user
            if user.id != Config.OWNER_ID:
                return 
            await func(client, message)

        return function

    @staticmethod
    def ADMIN(func):
        async def function(client, message):
            user = message.from_user
            if user.id not in (await list_admins(client, message.chat.id)):
                return 
            await func(client, message)

        return function

    @staticmethod
    def ANTI_USER():
        def decorator(func):
            return TB.on_message(filters.create(anti_chat_user) & ~filters.private)(func)
        return decorator

    @staticmethod
    def START(func):
        async def function(client, message):
            seved_users = await DB.get_list_vars(client.me.id, "start_users")
            user_id = message.from_user.id
            if user_id != Config.OWNER_ID:
                if user_id not in seved_users:
                    await DB.add_list_vars(client.me.id, "start_users", user_id)
            return await func(client, message)

        return function


