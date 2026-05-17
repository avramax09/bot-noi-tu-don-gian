import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")
timeout_seconds = int(os.getenv("TIMEOUT_SECONDS", "30"))

if not TOKEN:
    raise ValueError("TOKEN not found in environment variables. Please create noitu.env file from noitu.env.example")
