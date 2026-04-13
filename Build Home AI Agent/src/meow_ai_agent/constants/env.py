import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

def print_env():
    logger.info("Welcome {value}!", value=APP_NAME)
    logger.info("Current mode {value}!", value=DEV_MODE)