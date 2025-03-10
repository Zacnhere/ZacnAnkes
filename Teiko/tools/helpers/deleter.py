import string

from pyrogram import filters
from time import time

from Teiko import *


admins_in_chat = {}

async def list_admins(client, chat_id: int):
    global admins_in_chat
    
    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def isGcast(filter, client, update):
    with open('bl.txt') as file:
        blc = [w.lower().strip() for w in file.readlines()]

    bl_chars = "§∆π©®$€¥£¢"
    blc.extend(bl_chars)

    white_list = await DB.get_list_vars(TB.me.id, f"whitelist_{update.chat.id}") or []
    if update.from_user.id in white_list:
        return False

    if update.from_user.id in (await list_admins(client, update.chat.id)):
        return False

    bl_words = await DB.get_vars(TB.me.id, f"word_{update.chat.id}") or []
    if any(chara in update.text for chara in blc) or any(word in update.text for word in bl_words):
        return True

    return False

Ankes = filters.create(isGcast)
