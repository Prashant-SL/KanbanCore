import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE = os.getenv("AUTH_SERVICE")
BOARD_SERVICE = os.getenv("BOARD_SERVICE")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
RATE_LIMIT = os.getenv("RATE_LIMIT", "1000/minute")