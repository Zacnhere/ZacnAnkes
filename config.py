import os


class Config(object):
    API_ID = int(os.getenv("API_ID", "26761656"))
    API_HASH = os.getenv("API_HASH", "80dd784497f5fb01d74f2d2529fe3e8e")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7068529485:AAHevXamyL-PtSfvu5l-91D6BY9i4dwlwzo")
    OWNER_ID = int(os.getenv("OWNER_ID", "1361379181"))
    MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb+srv://ZacnAnkes:ZacnAnkes@cluster0.vcbtd.mongodb.net/?retryWrites=true&w=majority&appName=ZACNHERE",
    )

