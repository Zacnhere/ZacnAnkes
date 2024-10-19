from Teiko import *


class MSG:
    def START(message):
        return f"""
<b>👋🏻 Hai!</b>, <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<b>Selamat datang di</b> @{TB.me.username}
<b>Saya bot yang dapat menghapus pesan mengandung kata" terlarang!</b>

<b>Jika ingin menggunakan bot ini anda dapat membeli nya!</b>
"""

    def HELP(message):
        return """
<b>Menu Help Ankes!</b>

<b>Turn on or off Ankes!</b>
  /ankes <code>{on, off}</code>

<b>Add and remove Forbidden word!</b>
  /bl <code>{reply_message}</code>
  /rembl <code>{reply_message}</code>

<b>Adding or removing Anti-User!</b>
  /adduser <code>{reply, @, IDs}</code>
  /remuser <code>{reply, @, IDs}</code>
  /listuser
"""
    
