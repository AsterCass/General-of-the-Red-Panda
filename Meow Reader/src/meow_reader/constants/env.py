from dotenv import load_dotenv
from loguru import logger
import tomllib
from pathlib import Path
import os

load_dotenv()

def get_app_name():
    return os.getenv("APP_NAME")

def get_is_dev() -> bool:
    return os.getenv("DEV_MODE", "false").lower() == "true"

def print_env():
    APP_NAME = os.getenv("APP_NAME")
    DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

    logger.info("Welcome {value}!", value=APP_NAME)
    logger.info("Current model {value}!", value=DEV_MODE)


def print_config():
    path = Path("config.toml")

    if not path.exists():
        logger.warning(f"{path} not found.")
        return

    if not path.is_file():
        logger.error(f"{path} is not a file.")
        return

    try:
        with path.open("rb") as f:
            config = tomllib.load(f)

        logger.info("Read config")
        for section, content in config.items():
            logger.info(f"[{section}]")
            if isinstance(content, dict):
                for k, v in content.items():
                    logger.info(f"  {k} = {v}")
            else:
                logger.info(f"  {content}")

    except tomllib.TOMLDecodeError as e:
        logger.error(f"TOML Parse fail: {e}")