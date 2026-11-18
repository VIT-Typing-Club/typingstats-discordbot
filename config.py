import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/api/scores/typegg/daily")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing from .env")

if not DISCORD_CHANNEL_ID:
    raise ValueError("DISCORD_CHANNEL_ID is missing from .env")
