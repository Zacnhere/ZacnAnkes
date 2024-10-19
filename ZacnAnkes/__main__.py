import os
import asyncio

from Teiko import *


async def main():
    await TB.start()
    await asyncio.gather(loadPlugins(), exp_ankes())
    os.system("rm -rf *session*")
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
