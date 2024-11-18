from pyrogram import *

from Teiko import *


@PY.BOT("addwhite", filters.group)
@PY.ADMIN
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")
            
    try:
        user = await client.get_users(user_id)

        whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}") or []
        if user.id in whitelist:
            return await message.reply(f"<b>The user is already in the whitelist!</b>")
        
        blacklist = await DB.get_list_vars(TB.me.id, "blacklist") or []
        if user.id in blacklist:
            return await message.reply(f"<b>The user is registered in the blacklist!</b>")

        await DB.add_list_vars(TB.me.id, f"whitelist_{message.chat.id}", user.id)

        return await message.reply(
            f"<b>Added to whitelist:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:
        
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")


@PY.BOT("remwhite", filters.group)
@PY.ADMIN
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")
    
    try:
        user = await client.get_users(user_id)

        whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}") or []
        
        if user.id not in whitelist:
            return await message.reply(f"<b>The user is not in the whitelist!</b>")

        await DB.remove_list_vars(TB.me.id, f"whitelist_{message.chat.id}", user.id)

        return await message.reply(
            f"<b>Removed from whitelist:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:

        return await message.reply(f"<b>An error occurred:</b> {str(e)}")     


@PY.BOT("whitelist", filters.group)
@PY.ADMIN
async def _(client, message):
    x = await message.reply("<b>Processing...</b>")

    whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}")
    if not whitelist:
        return await x.edit("<b>Whitelist is empty!</b>")
    
    white = []
    for user_id in whitelist:
        try:
            user = await client.get_users(int(user_id))
            white.append(
                f"🔹 <b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b> | <code>{user.id}</code>"
            )
        except Exception:
            white.append(f"🔹 <code>{user_id}</code>")
            continue

    if white:
        response = (
            "<b>Whitelist Members:</b>\n\n" +
            "\n".join(white)
        )
        if len(response) > 4000:
            await x.edit("<b>Whitelist is too large to display here!</b>")
            return
        return await x.edit(response)
    else:
        return await x.edit("<b>Unable to retrieve the whitelist!</b>")   


@PY.BOT("ankes", filters.group)
@PY.ADMIN
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            "<b>Usage: /ankes on or /ankes off</b>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()
    
    if command not in query:
        return await message.reply(
            "<b>Invalid argument! Use 'on' or 'off'.</b>"
        )
    
    txt = (
        "<b>Ankes activated successfully!</b>"
        if command == "on"
        else "<b>Ankes deactivated successfully!</b>"
    )

    await DB.set_vars(TB.me.id, f"chat_{message.chat.id}", query[command])

    await message.reply(txt)
    


@PY.BOT("bl|addbl", filters.group)
@PY.ADMIN
async def _(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.reply("<b>Reply to message</b>")

    try:
        await add_word(client, message, text)
    except Exception as e:
        return await message.reply(f"Error: `{e}`")

    response = (
        f"<b>Successfully added prohibited words:</b>\n"
        f"{text}"
    )

    return await message.reply(response)


@PY.BOT("rembl|rbl", filters.group)
@PY.ADMIN
async def _(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.reply("<b>Reply to message</b>")

    try:
        await remove_word(client, message, text)
    except Exception as e:
        return await message.reply(f"Error: `{e}`")

    response = (
        f"<b>Successfully remove prohibited words:</b>\n"
        f"{text}"
    )

    return await message.reply(response)


async def add_word(client, message, text):
    bl_text = await DB.get_vars(TB.me.id, f"word_{message.chat.id}") or []
    bl_text.append(text)
    await DB.set_vars(TB.me.id, f"word_{message.chat.id}", bl_text)


async def remove_word(client, message, text):
    bl_text = await DB.get_vars(TB.me.id, f"word_{message.chat.id}") or []
    bl_text.remove(text)
    await DB.set_vars(TB.me.id, f"word_{message.chat.id}", bl_text)


@TB.on_message(filters.text & ~filters.private & Ankes)
async def _(client, message):
    text = "<b>Maaf, Grup ini tidak terdaftar di dalam list. Silahkan hubungi @shinteiko Untuk mendaftarkan Group Anda!</b>"
    chat_id = message.chat.id
    chats = await DB.get_list_vars(TB.me.id, "ankes_group")

    on_off_ankes = await DB.get_vars(TB.me.id, f"chat_{chat_id}")
    if not on_off_ankes:
        return

    if chat_id not in chats:
        await message.reply(text)
        await asyncio.sleep(30)
        return

    try:
        await message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await message.delete()
    except MessageDeleteForbidden:
        pass
    except Exception:
        await message.reply(f"<b>Error deleting message</b>")

