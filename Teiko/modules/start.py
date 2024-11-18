from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from Teiko import *

# Handle /start command for private chats
@PY.BOT("start", filters.private)
@PY.START
async def start_handler(client: Client, message: Message):
    try:
        msg = MSG.START(message)
        buttons = BTN.START(message)
        return await message.reply(msg, reply_markup=buttons)
    except Exception as e:
        return await message.reply(f"<b>An error occurred while processing your request:</b> {str(e)}")

# Handle "AH" callback query, possibly for a help section
@PY.CALLBACK("AH")
async def help_callback_handler(client: Client, callback_query: CallbackQuery):
    try:
        buttons = ikb([["| back - home |"]])  # Buttons for navigation
        return await callback_query.edit_message_text(
            MSG.HELP(callback_query),  # Dynamic message for help
            reply_markup=buttons,  # Dynamic buttons
        )
    except Exception as e:
        return await callback_query.answer(f"<b>An error occurred:</b> {str(e)}", show_alert=True)

# Handle "home" callback query to return to the home screen
@PY.CALLBACK("home")
async def home_callback_handler(client: Client, callback_query: CallbackQuery):
    try:
        buttons_home = BTN.START(callback_query)  # Dynamic home buttons
        return await callback_query.edit_message_text(
            MSG.START(callback_query),  # Dynamic home message
            reply_markup=buttons_home,  # Dynamic home buttons
        )
    except Exception as e:
        return await callback_query.answer(f"<b>An error occurred:</b> {str(e)}", show_alert=True)
