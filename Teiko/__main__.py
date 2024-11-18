import os
import asyncio
from Teiko import *

# Fungsi utama untuk memulai bot dan menjalankan plugin
async def main():
    # Memulai bot
    await TB.start()
    
    # Menjalankan plugin dan fungsi tambahan
    await asyncio.gather(loadPlugins(), exp_ankes())
    
    # Menghapus file session yang ada setelah bot dimulai
    os.system("rm -rf *session*")
    
    # Menunggu agar bot tetap berjalan
    await asyncio.Event().wait()

# Jika file ini dijalankan langsung, mulai event loop
if __name__ == "__main__":
    # Menggunakan asyncio.run untuk memulai aplikasi
    asyncio.run(main())
