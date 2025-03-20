from pyrogram import Client, filters
import os, sys, subprocess, platform, psutil
from io import BytesIO
import *


OWNER_ID = 1361379181  # Ganti dengan ID pemilik bot

@app.on_message(filters.command(["sh", "shutdown", "restart", "update", "clean", "host"]) & filters.user(OWNER_ID))
async def shell_command(client, message):
    command = message.command[1] if len(message.command) > 1 else None
    msg = await message.reply("🔄 <b>Processing...</b>", quote=True)
    
    if not command:
        return await msg.edit("<b>No command provided!</b>")
    
    try:
        if message.text.startswith("/shutdown"):
            await msg.delete()
            await handle_shutdown(message)
        elif message.text.startswith("/restart"):
            await msg.delete()
            await handle_restart(message)
        elif message.text.startswith("/update"):
            await msg.delete()
            await handle_update(message)
        elif message.text.startswith("/clean"):
            await handle_clean(message)
            await msg.delete()
        elif message.text.startswith("/host"):
            await handle_host(message)
            await msg.delete()
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await msg.edit(str(error))

async def handle_shutdown(message):
    await message.reply("✅ <b>System has been shut down.</b>", quote=True)
    os.system(f"kill -9 {os.getpid()}")

async def handle_restart(message):
    await message.reply("✅ <b>System is restarting...</b>", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "Teiko")

async def handle_update(message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    await message.reply(f"```{out}```", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "Teiko")

async def handle_clean(message):
    count = 0
    for file_name in os.popen("ls").read().split():
        try:
            os.remove(file_name)
            count += 1
        except:
            pass
    await message.reply(f"✅ {count} files cleaned.", quote=True)

async def process_command(message, command):
    result = subprocess.getoutput(command)
    if len(result) > 4096:
        await send_large_output(message, result)
    else:
        await message.reply(f"<code>{result}</code>", quote=True, parse_mode="html")

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
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_freq": cpufreq.max,
        "memory_total": svmem.total,
        "memory_used": svmem.used,
        "memory_percent": svmem.percent,
    }

def format_system_info(system_info):
    return (f"<b>System Information:</b>\n"
            f"System: {system_info['system']}\n"
            f"Release: {system_info['release']}\n"
            f"CPU Cores: {system_info['cpu_cores']}\n"
            f"CPU Max Frequency: {system_info['cpu_freq']} MHz\n"
            f"Memory Total: {system_info['memory_total']} bytes\n"
            f"Memory Used: {system_info['memory_used']} bytes\n"
            f"Memory Usage: {system_info['memory_percent']}%")
