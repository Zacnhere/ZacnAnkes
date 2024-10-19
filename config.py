import os


class Config(object):
    API_ID = int(os.getenv("API_ID", "24623085"))
    API_HASH = os.getenv("API_HASH", "75ce0c6125ae201c9e3d5a825c667a91")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7139966122:AAE6zafE_nDxGLttejwYW6YEGlqPCGaOPoU")
    OWNER_ID = int(os.getenv("OWNER_ID", "1825618929"))
    MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb+srv://trlynice:oc9VGD2dgYrKiQ5H@cluster0.tolyzhy.mongodb.net/?retryWrites=true&w=majority",
    )

