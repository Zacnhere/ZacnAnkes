import os
import platform
import subprocess
import sys
import traceback
import io
import asyncio
import time
import contextlib
import pyrogram
import html
import time
import uuid

from time import time
from datetime import date
from io import BytesIO, StringIO
from io import BytesIO
import psutil

from meval import meval
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from pyrogram import raw

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
)


import psutil

from Teiko import *

@PY.BOT("sh")
@PY.UBOT("sh")
async def _(client, message):
    if message.from_user.id != 1361379181:
        await message.reply_text(f"<b>ᴍᴀᴜ ɴɢᴀᴘᴀɪɴ ᴀɴᴊᴇɴᴋ?</b>")
        return
    command = get_arg(message)
    msg = await message.reply("🔄<b>ᴘʀᴏᴄᴇssɪɴɢ...</b>", quote=True)
    if not command:
        return await msg.edit("<b>ɴᴏᴏʙ</b>")
    try:
        if command == "shutdown":
            await msg.delete()
            await handle_shutdown(message)
        elif command == "restart":
            await msg.delete()
            await handle_restart(message)
        elif command == "update":
            await msg.delete()
            await handle_update(message)
        elif command == "clean":
            await handle_clean(message)
            await msg.delete()
        elif command == "host":
            await handle_host(message)
            await msg.delete() 
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await msg.edit(error)


async def handle_shutdown(message):
    await message.reply("<blockquote>✅ <b>ꜱʏꜱᴛᴇᴍ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴍᴀᴛɪᴋᴀɴ</b></blockquote>", quote=True)
    os.system(f"kill -9 {os.getpid()}")


async def handle_restart(message):
    await message.reply("<blockquote>✅ <b>ꜱʏꜱᴛᴇᴍ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ʀᴇꜱᴛᴀʀᴛ</b></blockquote>", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "PyroUbot")


async def handle_update(message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(out, quote=True)
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"```{out}```", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "PyroUbot")


async def handle_clean(message):
    count = 0
    for file_name in os.popen("ls").read().split():
        try:
            os.remove(file_name)
            count += 1
        except:
            pass
    await bash("rm -rf downloads")
    await message.reply(f"<blockquote><b>✅ {count} sᴀᴍᴘᴀʜ ʙᴇʀʜᴀsɪʟ ᴅɪ ʙᴇʀsɪʜᴋᴀɴ</b></blockquote>")


async def process_command(message, command):
    result = (await bash(command))[0]
    if int(len(str(result))) > 4096:
        await send_large_output(message, result)
    else:
        await message.reply(result)


async def send_large_output(message, output):
    with BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "result.txt"
        await message.reply_document(document=out_file)


async def handle_host(message):
    system_info = get_system_info()
    formatted_info = format_system_info(system_info)
    await message.reply(formatted_info, quote=True)


def get_system_info():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    return {
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "boot_time": psutil.boot_time(),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_total_cores": psutil.cpu_count(logical=True),
        "cpu_max_frequency": cpufreq.max,
        "cpu_min_frequency": cpufreq.min,
        "cpu_current_frequency": cpufreq.current,
        "cpu_percent_per_core": [
            percentage for percentage in psutil.cpu_percent(percpu=True)
        ],
        "cpu_total_usage": psutil.cpu_percent(),
        "network_upload": get_size(psutil.net_io_counters().bytes_sent),
        "network_download": get_size(psutil.net_io_counters().bytes_recv),
        "memory_total": get_size(svmem.total),
        "memory_available": get_size(svmem.available),
        "memory_used": get_size(svmem.used),
        "memory_percentage": svmem.percent,
    }



def format_system_info(system_info):
    formatted_info = "Informasi Sistem\n"
    formatted_info += f"Sistem   : {system_info['system']}\n"
    formatted_info += f"Rilis    : {system_info['release']}\n"
