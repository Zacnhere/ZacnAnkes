import asyncio
from datetime import datetime
from pytz import timezone
from Teiko import *


async def exp_ankes():
    while True:
        # Mendapatkan waktu sekarang di zona waktu Asia/Jakarta
        current_time = datetime.now(timezone("Asia/Jakarta"))
        
        # Mengambil daftar chat_id yang terdaftar di "ankes_group"
        chats = await DB.get_list_vars(TB.me.id, "ankes_group")
        
        for chat_id in chats:
            try:
                # Mengambil tanggal kadaluwarsa untuk chat_id ini
                exp_date_str = await DB.get_exp(chat_id)
                
                if exp_date_str:
                    # Coba parsing tanggal kadaluwarsa dari string
                    try:
                        exp_date = datetime.strptime(exp_date_str, "%d.%m.%Y")
                    except ValueError as e:
                        print(f"Invalid expiration date format for chat_id {chat_id}: {exp_date_str}")
                        continue
                    
                    # Mengecek apakah tanggal kadaluwarsa sudah sama dengan tanggal saat ini
                    if current_time.date() == exp_date.date():
                        # Hapus masa aktif
                        await DB.rem_exp(chat_id)
                        await DB.set_vars(TB.me.id, f"chat_{chat_id}", False)
                        await DB.remove_list_vars(TB.me.id, "ankes_group", chat_id)
                        
                        # Kirim pesan pemberitahuan ke chat bahwa masa aktif telah habis
                        await TB.send_message(
                            chat_id,
                            f"<b>Masa Aktif telah habis, jika ingin memperpanjang masa aktif silakan hubungi @shinteiko !!!</b>"
                        )
            except Exception as e:
                # Menangani kesalahan lain yang mungkin terjadi saat memproses chat_id
                print(f"Error processing chat_id {chat_id}: {e}")
                try:
                    # Jika terjadi kesalahan, pastikan menghapus data terkait
                    await DB.rem_exp(chat_id)
                    await DB.set_vars(TB.me.id, f"chat_{chat_id}", False)
                    await DB.remove_list_vars(TB.me.id, "ankes_group", chat_id)
                    await TB.send_message(
                        chat_id,
                        f"<b>Masa Aktif telah habis, jika ingin memperpanjang masa aktif silakan hubungi @shinteiko !!!</b>"
                    )
                except Exception as inner_error:
                    print(f"Error during cleanup for chat_id {chat_id}: {inner_error}")
                    
        # Tunggu selama 60 detik sebelum memeriksa kembali
        await asyncio.sleep(60)

# Fungsi utama yang dapat dijalankan secara asynchronous
async def main():
    # Memulai proses exp_ankes yang berjalan terus menerus
    await exp_ankes()

# Pastikan event loop berjalan ketika file ini dijalankan
if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
