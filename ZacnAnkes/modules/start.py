from pyrogram import *
from pyrogram.types import *

from Teiko import *



@PY.BOT("start", filters.private)
@PY.START
async def _(client, message):
    msg = MSG.START(message)
    buttons = BTN.START(message)
    return await message.reply(msg, reply_markup=buttons)


@PY.CALLBACK("AH")
async def _(client, callback_query):
    buttons = ikb([
        ["| back - home |"]
    ])
    return await callback_query.edit_message_text(
        MSG.HELP(callback_query),
        reply_markup=buttons,
    )


@PY.CALLBACK("home")
async def _(client, callback_query):
    buttons_home = BTN.START(callback_query)
    return await callback_query.edit_message_text(
        MSG.START(callback_query),
        reply_markup=buttons_home,
    )

