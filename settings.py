from envparse import Env
from loguru import logger

env = Env()
env.read_envfile(".env")
LOGER = logger
LOGER.add(
    "logs/logs.log",
    rotation="10 KB",
    format="{time} {level} {message}",
    level="ERROR"
)

MONGO_PORT = env.int("MONGO_PORT")
MONGO_USER = env.str("MONGO_USER")
MONGO_PASS = env.str("MONGO_PASS")
TOKEN_BOT = env.str("TOKEN_BOT")
MONGO_URL = env.str("MONGO_URL", default=f"mongodb://0.0.0.0:{MONGO_PORT}")
