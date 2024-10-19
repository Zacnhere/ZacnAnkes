import os


class Config(object):
    API_ID = int(os.getenv("API_ID", "24623085"))
    API_HASH = os.getenv("API_HASH", "75ce0c6125ae201c9e3d5a825c667a91")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7068529485:AAHevXamyL-PtSfvu5l-91D6BY9i4dwlwzo")
    OWNER_ID = int(os.getenv("OWNER_ID", "1361379181"))
    MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb+srv://ZacnAnkes:ZacnAnkes@cluster0.vcbtd.mongodb.net/?retryWrites=true&w=majority&appName=ZACNHERE",
    )

