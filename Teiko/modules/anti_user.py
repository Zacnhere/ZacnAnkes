import asyncio
from config import Config
from Teiko import *
from pyrogram.errors import FloodWait, MessageDeleteForbidden

# Menambahkan pengguna ke daftar Anti-User
@PY.BOT("adduser", filters.group)
@PY.OWNER
async def add_user_to_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply ke pengguna atau berikan ID/username yang valid!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>Pengguna ini adalah pemilik bot!</b>")

    try:
        user = await client.get_users(user_id)
        anti_users = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        
        if str(user.id) in anti_users:
            return await message.reply(f"<b>Pengguna sudah ada dalam daftar Anti-User!</b>")

        await DB.add_list_vars(TB.me.id, "anti_message_user", str(user.id))
        return await message.reply(
            f"<b>Ditambahkan ke daftar Anti-User:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:
        return await message.reply(f"<b>Terjadi kesalahan:</b> {str(e)}")

# Menghapus pengguna dari daftar Anti-User
@PY.BOT("remuser", filters.group)
@PY.OWNER
async def remove_user_from_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply ke pengguna atau berikan ID/username yang valid!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>Pengguna ini adalah pemilik bot!</b>")

    try:
        user = await client.get_users(user_id)
        anti_users = await DB.get_list_vars(TB.me.id, "anti_message_user") or []

        if str(user.id) not in anti_users:
            return await message.reply("<b>Pengguna tidak ada dalam daftar Anti-User!</b>")

        await DB.remove_list_vars(TB.me.id, "anti_message_user", str(user.id))
        return await message.reply(
            f"<b>Dihapus dari daftar Anti-User:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
        )
    except Exception as e:
        return await message.reply(f"<b>Terjadi kesalahan:</b> {str(e)}")

# Menampilkan daftar Anti-User dengan pagination
@PY.BOT("listuser", filters.group)
@PY.OWNER
async def list_anti_users(client, message):
    x = await message.reply("<b>Memproses...</b>")

    anti_users = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
    if not anti_users:
        return await x.edit("<b>Tidak ada pengguna dalam daftar Anti-User!</b>")

    if message.from_user.id not in (await list_admins(client, message.chat.id)):
        return await x.edit("<b>Anda bukan admin dalam grup ini!</b>")

    # Pagination
    PAGE_SIZE = 5  
    page = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 1
    total_pages = (len(anti_users) + PAGE_SIZE - 1) // PAGE_SIZE
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    white = []
    for user_id in anti_users[start_index:end_index]:
        try:
            user = await client.get_users(int(user_id))
            white.append(f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>")
        except Exception:
            white.append(f"<code>{user_id}</code>")
            continue

    if white:
        response = f"<b>Daftar Anti-User (Halaman {page}/{total_pages}):</b>\n\n" + "\n".join(white)
        if total_pages > 1:
            response += f"\n\n<b>Gunakan /listuser {page + 1} untuk melihat halaman berikutnya</b>" if page < total_pages else ""
        return await x.edit(response)
    else:
        return await x.edit("<b>Tidak ada pengguna ditemukan dalam daftar Anti-User!</b>")

# Menghapus pesan dari pengguna dalam daftar Anti-User


@PY.ANTI_USER()
async def handle_anti_user_message(client, message):
    try:
        # Mengecek apakah bot memiliki izin untuk menghapus pesan
        chat_permissions = await check_permissions(client, message.chat.id)
        if not chat_permissions:
            return await message.reply("<b>Saya tidak memiliki izin untuk menghapus pesan dalam grup ini.</b>")

        await message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await message.delete()
        except Exception as r:
            await message.reply(f"<b>Gagal menghapus pesan dari Anti-User:</b> {str(r)}")
    except MessageDeleteForbidden:
        await message.reply("<b>Saya tidak memiliki izin untuk menghapus pesan dalam grup ini.</b>")
    except Exception as e:
        await message.reply(f"<b>Terjadi kesalahan:</b> {str(e)}")

# Mendapatkan daftar admin grup
async def list_admins(client, chat_id):
    chat_members = await client.get_chat_members(chat_id)
    return [member.user.id for member in chat_members if member.status in ['administrator', 'creator']]

# Mengecek apakah bot memiliki izin menghapus pesan
async def check_permissions(client, chat_id):
    chat = await client.get_chat(chat_id)
    return chat.permissions.can_delete_messages if chat.permissions else False
