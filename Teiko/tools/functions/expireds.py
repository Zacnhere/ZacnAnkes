import asyncio

from datetime import datetime
from pytz import timezone

from Teiko import *


async def exp_ankes():
    while True:
        current_time = datetime.now(timezone("Asia/Jakarta"))
        chats = await DB.get_list_vars(TB.me.id, "ankes_group")
        for chat_id in chats:
            try:
                exp_date_str = await DB.get_exp(chat_id)
                if exp_date_str:
                    exp_date = datetime.strptime(exp_date_str, "%d.%m.%Y")
                    if current_time.date() == exp_date.date():
                        await DB.rem_exp(chat_id)
                        await DB.set_vars(TB.me.id, f"chat_{chat_id}", False)
                        await DB.remove_list_vars(TB.me.id, "ankes_group", chat_id)
                        await TB.send_message(chat_id, f"<b>Masa Aktif telah habis, jika ingin memperpanjang masa aktif silakan hubungi @zacnboys !!!</b>")
            except Exception as e:
                print(f"Error processing chat_id {chat_id}: {e}")
                await DB.rem_exp(chat_id)
                await DB.set_vars(TB.me.id, f"chat_{chat_id}", False)
                await DB.remove_list_vars(TB.me.id, "ankes_group", chat_id)
                await TB.send_message(chat_id, f"<b>Masa Aktif telah habis, jika ingin memperpanjang masa aktif silakan hubungi @zacnboys !!!</b>")
        await asyncio.sleep(60)
