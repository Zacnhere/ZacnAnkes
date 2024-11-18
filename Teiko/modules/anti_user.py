from config import Config
from Teiko import *
from pyrogram.errors import FloodWait, MessageDeleteForbidden

# Adding a user to the Anti-User list
@PY.BOT("adduser", filters.group)
@PY.OWNER
async def add_user_to_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if user_id in anti:
            return await message.reply(f"<b>User is already in Anti-User list!</b>")

        await DB.add_list_vars(TB.me.id, "anti_message_user", user.id)
        return await message.reply(f"<b>Added to Anti-User list:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")

    except Exception as e:
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

# Removing a user from the Anti-User list
@PY.BOT("remuser", filters.group)
@PY.OWNER
async def remove_user_from_anti_list(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")

    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
        if user_id not in anti:
            return await message.reply("<b>User is not in Anti-User list!</b>")

        await DB.remove_list_vars(TB.me.id, "anti_message_user", user.id)
        return await message.reply(f"<b>Removed from Anti-User list:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")

    except Exception as e:
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")

# Listing Anti-User entries with pagination support
@PY.BOT("listuser", filters.group)
@PY.OWNER
async def list_anti_users(client, message):
    x = await message.reply("<b>Processing...</b>")
    
    whitelist = await DB.get_list_vars(TB.me.id, "anti_message_user") or []
    if not whitelist:
        return await x.edit("<b>No users in Anti-User list!</b>")
    
    if message.from_user.id not in (await list_admins(client, message.chat.id)):
        return await x.edit("<b>You are not an admin in this group!</b>")

    # Pagination handling
    PAGE_SIZE = 5  # Number of users per page
    page = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 1
    total_pages = (len(whitelist) + PAGE_SIZE - 1) // PAGE_SIZE
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    # Display users for the current page
    white = []
    for user_id in whitelist[start_index:end_index]:
        try:
            user = await client.get_users(int(user_id))
            white.append(
                f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except Exception:
            white.append(f"<code>{user_id}</code>")
            continue

    if white:
        response = (
            f"<b>Anti-User List (Page {page}/{total_pages}):</b>\n\n" +
            "\n".join(white) +
            f"\n\n<b>Page {page} of {total_pages}</b>"
        )
        if total_pages > 1:
            response += f"\n\n<b>Use /listuser {page + 1} to see the next page</b>" if page < total_pages else ""
        return await x.edit(response)
    else:
        return await x.edit("<b>No users found in the Anti-User list!</b>")

# Automatically deleting messages from Anti-Users
@PY.ANTI_USER()
async def handle_anti_user_message(client, message):
    try:
        await message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)
        try:
            await message.delete()
        except Exception as r:
            await message.reply(f"<b>Failed to delete message from anti-user:</b> {str(r)}")
    except MessageDeleteForbidden:
        await message.reply("<b>I don't have permission to delete messages in this group.</b>")
    except Exception as e:
        await message.reply(f"<b>An error occurred:</b> {str(e)}")

# Utility functions for managing permissions and list checking
async def list_admins(client, chat_id):
    chat_members = await client.get_chat_members(chat_id)
    return [member.user.id for member in chat_members if member.status in ['administrator', 'creator']]

# Ensure the bot has the necessary permissions
async def check_permissions(client, chat_id):
    chat = await client.get_chat(chat_id)
    if not chat.can_delete_messages:
        return False
    return True
