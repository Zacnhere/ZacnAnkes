from config import Config

from Teiko import *



@PY.BOT("adduser", filters.group)
@PY.OWNER
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")

    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")
        
    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user")
        if user_id in anti:
            return await message.reply(f"<b>Already on Anti-user!</b>")
            
        await DB.add_list_vars(TB.me.id, "anti_message_user", user.id)
        return await message.reply(f"<b>Adding to Anti-User!</b>  [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")
    except Exception as e:
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")


@PY.BOT("remuser", filters.group)
@PY.OWNER
async def _(client, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("<b>Reply to a user or provide a valid ID/username!</b>")
            
    if user_id == Config.OWNER_ID:
        return await message.reply("<b>The user is the owner!</b>")
    try:
        user = await client.get_users(user_id)
        anti = await DB.get_list_vars(TB.me.id, "anti_message_user")
        if user_id not in anti:
            return await message.reply(f"<b>Not in whitelist!</b>")
        await DB.remove_list_vars(TB.me.id, "anti_message_user", user.id)
        return await message.reply(f"<b>Remove to Anti-User!</b>  [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})")
    except Exception as e:
        return await message.reply(f"<b>An error occurred:</b> {str(e)}")


@PY.BOT("listuser", filters.group)
@PY.OWNER
async def _(client, message):
    x = await message.reply("<b>Processing...</b>")
    whitelist = await DB.get_list_vars(TB.me.id, "anti_message_user")
    if not whitelist:
        return await x.edit("<b>Anti-User empty!</b>")
    if message.from_user.id not in (await list_admins(client, message.chat.id)):
        return await x.edit("<b>You are not an admin in this group!</b>")
    white = []
    for user_id in whitelist:
        try:
            user = await client.get_users(int(user_id))
            white.append(
                f"<b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            white.append(f"<code>{user.id}</code>")
            continue
    if white:
        response = (
            "<b>Anti-User!</b>\n\n"
            + "\n".join(white)
        )
        return await x.edit(response)
    else:
        return await x.edit("<b>Unable to retrieve list!</b>")


@PY.ANTI_USER()
async def _(client, message):
    try:
        await message.delete()
    except Exception as r:
        await message.delete()

