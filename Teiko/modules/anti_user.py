from config import Config
from Teiko import *

@PY.BOT("adduser", filters.group)
@PY.ADMIN
async def _(client, message):
    try:
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")
        
        user_id = int(user_id)  # Pastikan user_id dalam bentuk integer
        if user_id == Config.OWNER_ID:
            return await message.reply("<b>The user is the owner!</b>")
        
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        
        if user_id in anti:
            return await message.reply("<b>Already on Anti-user!</b>")
        
        await DB.add_list_vars(TB.me.id, "anti_message_user", user_id)
        return await message.reply(f"<b>Adding to Anti-User!</b>  [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")
    except Exception as e:
        print(f"Error in /adduser: {e}")  # Logging untuk debugging
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

@PY.BOT("remuser", filters.group)
@PY.ADMIN
async def _(client, message):
    try:
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")
        
        user_id = int(user_id)
        if user_id == Config.OWNER_ID:
            return await message.reply("<b>The user is the owner!</b>")
        
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if user_id not in anti:
            return await message.reply("<b>Not in whitelist!</b>")
        
        await DB.remove_list_vars(TB.me.id, "anti_message_user", user_id)
        return await message.reply(f"<b>Removed from Anti-User!</b> <code>{user_id}</code>")
    except Exception as e:
        print(f"Error in /remuser: {e}")
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

@PY.BOT("listuser", filters.group)
@PY.ADMIN
async def _(client, message):
    try:
        x = await message.reply("<b>Processing...</b>")
        whitelist = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if not whitelist:
            return await x.edit("<b>Anti-User list is empty!</b>")
        
        admins = await list_admins(client, message.chat.id)
        if message.from_user.id not in admins:
            return await x.edit("<b>You are not an admin in this group!</b>")
        
        white = []
        for user_id in whitelist:
            try:
                user = await client.get_users(int(user_id))
                white.append(f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>")
            except Exception as e:
                print(f"Error fetching user {user_id}: {e}")
                white.append(f"<code>{user_id}</code>")
        
        response = "<b>Anti-User List:</b>\n\n" + "\n".join(white)
        return await x.edit(response)
    except Exception as e:
        print(f"Error in /listuser: {e}")
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

@PY.ANTI_USER()
async def _(client, message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Error in ANTI_USER: {e}")
