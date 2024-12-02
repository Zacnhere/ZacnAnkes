from pyrogram import *

from Teiko import *


@PY.BOT("addwhite", filters.group)
@PY.ADMIN
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>ᴍᴏʜᴏɴ ʀᴇᴘʟʏ ᴀᴛᴀᴜ ᴜsᴇʀɴᴀᴍᴇ ᴘᴇɴɢɢᴜɴᴀ!</b>")
            
    try:
        user = await client.get_users(user_id)

        whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}") or []
        if user.id in whitelist:
            return await message.reply(f"<b>ᴘᴇɴɢɢᴜɴᴀ sᴜᴅᴀʜ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ</b>")
        
        blacklist = await DB.get_list_vars(TB.me.id, "blacklist") or []
        if user.id in blacklist:
            return await message.reply(f"<b>ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʀᴅᴀғᴛᴀʀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ</b>")

        await DB.add_list_vars(TB.me.id, f"whitelist_{message.chat.id}", user.id)

        return await message.reply(
            f"<b>ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:
        
        return await message.reply(f"<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:</b> {str(e)}")


@PY.BOT("delwhite", filters.group)
@PY.ADMIN
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>ᴍᴏʜᴏɴ ʀᴇᴘʟʏ ᴀᴛᴀᴜ ᴜsᴇʀɴᴀᴍᴇ ᴘᴇɴɢɢᴜɴᴀ!</b>")
    
    try:
        user = await client.get_users(user_id)

        whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}") or []
        
        if user.id not in whitelist:
            return await message.reply(f"<b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ</b>")

        await DB.remove_list_vars(TB.me.id, f"whitelist_{message.chat.id}", user.id)

        return await message.reply(
            f"<b>ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:

        return await message.reply(f"<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:</b> {str(e)}")     


@PY.BOT("whitelist", filters.group)
@PY.ADMIN
async def _(client, message):
    x = await message.reply("<b>ᴍᴇᴍᴘᴏsᴇs...</b>")

    whitelist = await DB.get_list_vars(TB.me.id, f"whitelist_{message.chat.id}")
    if not whitelist:
        return await x.edit("<b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ</b>")
    
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
            "<b>ᴛᴀᴍᴘɪʟᴀɴ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ:</b>\n\n" +
            "\n".join(white)
        )
        if len(response) > 4000:
            await x.edit("<b>ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ ᴛᴇʀʟᴀʟᴜ ʙᴇsᴀʀ\n ᴜɴᴛᴜᴋ ᴅɪᴛᴀᴍᴘɪʟᴋᴀɴ ᴅɪ sɪɴɪ</b>")
            return
        return await x.edit(response)
    else:
        return await x.edit("<b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀғᴛᴀʀ ᴘᴜᴛɪʜ</b>")   


@PY.BOT("ankes", filters.group)
@PY.ADMIN
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            "<b>ɢᴜɴᴀᴋᴀɴ: /ᴀɴᴋᴇs ᴏɴ ᴀᴛᴀᴜ /ᴀɴᴋᴇs ᴏғғ</b>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()
    
    if command not in query:
        return await message.reply(
            "<b>ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ! ɢᴜɴᴀᴋᴀɴ 'ᴏɴ' ᴀᴛᴀᴜ 'ᴏғғ'.</b>"
        )
    
    txt = (
        "<b>ᴍᴇɴʏᴀʟᴀ ᴀʙᴀɴɢ ᴋᴜ</b>"
        if command == "on"
        else "<b>sɪsᴛᴇᴍ ᴅɪɴᴏɴᴀᴋᴛɪғᴋᴀɴ</b>"
    )

    await DB.set_vars(TB.me.id, f"chat_{message.chat.id}", query[command])

    await message.reply(txt)
    

@PY.BOT("bl", filters.group)
@PY.ADMIN
async def add_to_blacklist(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.reply("<b>ᴘᴇsᴀɴ ɴʏᴀ ᴍᴀɴᴀ ᴛᴏᴅ</b>")

    try:
        await add_word(client, message, text)
    except Exception as e:
        return await message.reply(f"Error: `{e}`")

    response = (
        f"<b>ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴋᴀᴛᴀ ʙᴜsᴜᴋ ᴋᴇᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ:</b>\n"
        f"{text}"
    )

    return await message.reply(response)


@PY.BOT("unbl", filters.group)
@PY.ADMIN
async def remove_from_blacklist(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    else:
        return await message.reply("<b>Reply to a message to remove it from the blacklist.</b>")

    try:
        await remove_word(client, message, text)
    except ValueError:
        return await message.reply("<b>Word not found in blacklist.</b>")
    except Exception as e:
        return await message.reply(f"Error: `{e}`")

    response = (
        f"<b>Successfully removed prohibited words:</b>\n"
        f"{text}"
    )

    return await message.reply(response)


async def add_word(client, message, text):
    # Mendapatkan daftar kata blacklist yang ada
    bl_text = await DB.get_vars(TB.me.id, f"word_{message.chat.id}") or []
    
    # Validasi untuk mencegah duplikasi
    if text in bl_text:
        raise ValueError("Word already exists in blacklist.")
    
    # Menambahkan kata baru ke daftar
    bl_text.append(text)
    await DB.set_vars(TB.me.id, f"word_{message.chat.id}", bl_text)


async def remove_word(client, message, text):
    # Mendapatkan daftar kata blacklist yang ada
    bl_text = await DB.get_vars(TB.me.id, f"word_{message.chat.id}") or []
    
    # Menghapus kata dari daftar
    bl_text.remove(text)  # Akan memunculkan ValueError jika kata tidak ditemukan
    await DB.set_vars(TB.me.id, f"word_{message.chat.id}", bl_text)
        

@TB.on_message(filters.text & ~filters.private & Ankes)
async def handle_message(client, message):
    # Pesan default jika grup tidak terdaftar
    default_text = (
        "<b>Maaf, Grup ini tidak terdaftar dalam daftar. Silahkan hubungi @shinteiko "
        "untuk mendaftarkan grup Anda!</b>"
    )

    chat_id = message.chat.id

    # Memeriksa apakah fitur Ankes aktif untuk grup
    on_off_ankes = await DB.get_vars(TB.me.id, f"chat_{chat_id}")
    if not on_off_ankes:
        return

    # Memeriksa apakah grup ada dalam daftar yang diizinkan
    chats = await DB.get_list_vars(TB.me.id, "ankes_group")
    if chat_id not in chats:
        await message.reply(default_text)
        await asyncio.sleep(30)
        return

    # Mencoba menghapus pesan pengguna
    try:
        await message.delete()
    except FloodWait as e:
        # Tunggu jika ada pembatasan FloodWait
        await asyncio.sleep(e.x)
        try:
            await message.delete()
        except Exception as inner_error:
            await message.reply(f"<b>Gagal menghapus pesan: {str(inner_error)}</b>")
    except MessageDeleteForbidden:
        # Jika bot tidak memiliki izin untuk menghapus pesan
        await message.reply(
            "<b>Saya tidak memiliki izin untuk menghapus pesan di grup ini. "
            "Pastikan bot memiliki izin yang benar.</b>"
        )
    except Exception as e:
        # Penanganan kesalahan umum
        await message.reply(f"<b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:</b> {str(e)}")
