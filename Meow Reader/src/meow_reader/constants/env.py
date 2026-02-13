import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def get_app_name():
    return os.getenv("APP_NAME")

def get_is_dev() -> bool:
    return os.getenv("DEV_MODE", "false").lower() == "true"

def print_env():
    APP_NAME = os.getenv("APP_NAME")
    DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

    logger.info("Welcome {value}!", value=APP_NAME)
    logger.info("Current mode {value}!", value=DEV_MODE)