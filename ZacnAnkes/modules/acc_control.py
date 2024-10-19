
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from pyrogram.errors import *

from datetime import datetime, timedelta
from pytz import timezone

from Teiko import *


@PY.BOT("profile")
async def _(client, message):
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        return await message.reply("<b>Usage chat_id or @ group!</b>")

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await message.reply("<b>Group not found!</b>")
    try:
        chat = await client.get_chat(chat_id)
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        else:
            response = f"{chat_id}"
        exp = await DB.get_exp(chat_id)
        if exp:
            time = exp
        else:
            time = "Null"
        status = await DB.get_vars(TB.me.id, f"chat_{chat_id}")
        await message.reply(f"""
<b>Profiles Ankes!</b>

 <b>Group:</b> {response}
 <b>Status:</b> {status}
 <b>Expired:</b> {time}
""")
    except Exception as error:
        await message.reply(error)


@PY.BOT("addankes")
async def _(client, message):
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
            get_day = int(message.command[2]) if len(message.command) > 2 else 30
        else:
            return await message.reply("<b>Usage: /command chat_id or @group [days]</b>")

        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await message.reply("<b>You do not have access to use this command here.</b>")

        chat_id = await extract_id(message, input_identifier)
        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        chat = await client.get_chat(chat_id)

        if not chat.id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")
            
        if chat.id in ankes:
            return await message.reply("<b>Group chat is already in the ankes list!</b>")

        expiry_date = (datetime.now() + timedelta(days=get_day)).strftime("%d.%m.%Y")
        await DB.add_exp(chat.id, expiry_date)
        await DB.add_list_vars(TB.me.id, "ankes_group", chat.id)

        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        else:
            response = f"{chat.id}"

        message_content = f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Expired:</b> {get_day} day(s)
<b>Reason:</b> Added to ankes list
"""
        return await message.reply(message_content)

    except ValueError:
        return await message.reply("<b>Error: Invalid number of days provided. Please provide a valid integer.</b>")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@PY.BOT("remankes")
async def _(client, message):
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            return await message.reply("<b>Usage: /command chat_id or @group</b>")

        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await message.reply("<b>You do not have access to use this command here.</b>")

        chat_id = await extract_id(message, input_identifier)
        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        chat = await client.get_chat(chat_id)
        
        if not chat.id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")
        
        if chat.id not in ankes:
            return await message.reply("<b>Group chat is not in the ankes list!</b>")
        
        await DB.rem_exp(chat.id)
        await DB.remove_list_vars(TB.me.id, "ankes_group", chat.id)
        
        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        else:
            response = f"{chat.id}"
        
        message_content = f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Expired:</b> Null
<b>Reason:</b> Removed from ankes list
"""
        return await message.reply(message_content)

    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@PY.BOT("listankes|lankes")
async def _(client, message):
    mzg = await message.reply("<b>Processing...</b>")

    try:
        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await mzg.edit("<b>You do not have access to use this command here.</b>")

        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        if not ankes:
            return await mzg.edit("<b>Ankes group list is empty!</b>")

        chat_list = []
        for chat_id in ankes:
            try:
                chat = await client.get_chat(int(chat_id))
                if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    chat_list.append(
                        f'<a href="https://t.me/{chat.username or chat.id}">{chat.title}</a>'
                    )
            except Exception as e:
                chat_list.append(f"<code>{chat_id}</code>")
                continue

        if chat_list:
            response = "<b>Ankes Group List:</b>\n\n" + "\n".join(chat_list)
            return await mzg.edit(response)
        else:
            return await mzg.edit("<b>No valid groups found in the Ankes list!</b>")
    
    except Exception as e:
        return await mzg.edit(f"<b>An unexpected error occurred:</b> {str(e)}")

