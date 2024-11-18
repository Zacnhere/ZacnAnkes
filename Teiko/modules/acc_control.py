from pyrogram import filters
from pyrogram.enums import ChatType
from datetime import datetime, timedelta
import asyncio

@PY.BOT("profile")
async def profile_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage: /profile [chat_id or @group]</b>")

    input_identifier = message.command[1]
    chat_id = await extract_id(message, input_identifier)

    if not chat_id:
        return await message.reply("<b>Group not found!</b>")

    try:
        chat = await client.get_chat(chat_id)
        response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        exp = await DB.get_exp(chat_id) or "Null"
        status = await DB.get_vars(TB.me.id, f"chat_{chat_id}") or "Inactive"

        return await message.reply(f"""
<b>Profiles Ankes!</b>

<b>Group:</b> {response}
<b>Status:</b> {status}
<b>Expired:</b> {exp}
""")
    except Exception as e:
        return await message.reply(f"<b>Error:</b> {str(e)}")


@PY.BOT("addankes")
async def add_ankes_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage: /addankes [chat_id or @group] [days]</b>")

    try:
        input_identifier = message.command[1]
        get_day = int(message.command[2]) if len(message.command) > 2 else 30

        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await message.reply("<b>You do not have access to use this command.</b>")

        chat_id = await extract_id(message, input_identifier)
        if not chat_id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")

        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        if chat_id in ankes:
            return await message.reply("<b>Group is already in the Ankes list!</b>")

        expiry_date = (datetime.now() + timedelta(days=get_day)).strftime("%d.%m.%Y")
        await DB.add_exp(chat_id, expiry_date)
        await DB.add_list_vars(TB.me.id, "ankes_group", chat_id)

        chat = await client.get_chat(chat_id)
        response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"

        return await message.reply(f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Expired:</b> {expiry_date}
<b>Reason:</b> Added to Ankes list
""")
    except ValueError:
        return await message.reply("<b>Error: Invalid number of days provided.</b>")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@PY.BOT("remankes")
async def remove_ankes_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage: /remankes [chat_id or @group]</b>")

    try:
        input_identifier = message.command[1]

        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await message.reply("<b>You do not have access to use this command.</b>")

        chat_id = await extract_id(message, input_identifier)
        if not chat_id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")

        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        if chat_id not in ankes:
            return await message.reply("<b>Group is not in the Ankes list!</b>")

        await DB.rem_exp(chat_id)
        await DB.remove_list_vars(TB.me.id, "ankes_group", chat_id)

        chat = await client.get_chat(chat_id)
        response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"

        return await message.reply(f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Expired:</b> Null
<b>Reason:</b> Removed from Ankes list
""")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@PY.BOT("listankes|lankes")
async def list_ankes_handler(client, message):
    mzg = await message.reply("<b>Processing...</b>")

    try:
        if message.from_user.id not in (Config.OWNER_ID, *await DB.get_list_vars(TB.me.id, "seller")):
            return await mzg.edit("<b>You do not have access to use this command.</b>")

        ankes = await DB.get_list_vars(TB.me.id, "ankes_group")
        if not ankes:
            return await mzg.edit("<b>Ankes group list is empty!</b>")

        chat_list = []
        for chat_id in ankes:
            try:
                chat = await client.get_chat(int(chat_id))
                response = f'<a href="https://t.me/{chat.username or chat.id}">{chat.title}</a>'
                chat_list.append(response)
            except Exception:
                chat_list.append(f"<code>{chat_id}</code>")
                continue

        return await mzg.edit("<b>Ankes Group List:</b>\n\n" + "\n".join(chat_list))
    except Exception as e:
        return await mzg.edit(f"<b>An unexpected error occurred:</b> {str(e)}")
