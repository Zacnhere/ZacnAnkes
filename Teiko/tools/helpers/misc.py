import base64

from pyrogram import *
from pyrogram.enums import *

from Teiko import *



def get_arg(message):
    if message.reply_to_message and len(message.command) < 2:
        msg = message.reply_to_message.text or message.reply_to_message.caption
        if not msg:
            return ""
        msg = msg.encode().decode("UTF-8")
        msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
        return msg
    elif len(message.command) > 1:
        return " ".join(message.command[1:])
    else:
        return ""


def type_and_msg(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None
    
    type = args[1]
    msg = message.reply_to_message if message.reply_to_message else args[2] if len(args) > 2 else None
    return type, msg


async def gcast_type(client, query):
    if query == "user":
        db_users = await DB.get_list_vars(TB.me.id, "start_users")
        return db_users

    elif query == "group":
        db_group = await DB.get_list_vars(TB.me.id, "ankes_group")
        return db_group

    else:
        return []


async def extract_id(message, text):
    def is_int(text):
        try:
            return int(text)
        except ValueError:
            return None

    text = text.strip() if text else ''

    chat_id = is_int(text)
    if chat_id is not None:
        if str(chat_id).startswith('-') or chat_id > 0:
            return chat_id

    app = message._client
    entities = message.entities

    if entities:
        entity = entities[1 if message.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            try:
                user = await app.get_chat(text)
                return user.id
            except Exception:
                return None
        elif entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
            
    if text.startswith('@'):
        try:
            chat = await app.get_chat(text)
            return chat.id
        except Exception:
            return None

    return None


async def extract_user(message, sender_chat=False):
    args = message.text.strip().split()

    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.sender_chat and sender_chat:
            return reply.sender_chat.id
        elif reply.from_user:
            return reply.from_user.id
        else:
            return None

    if len(args) >= 2:
        user_id = await extract_id(message, args[1])
        return user_id

    return None
