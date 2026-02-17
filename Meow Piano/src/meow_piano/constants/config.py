import tomllib
from pathlib import Path

from loguru import logger

data_path = Path("data/data.db")

def load_config():
    path = Path("config.toml")
    global data_path

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
                    if k == "dbPath":
                        data_path = v
                        logger.info(f"DB path: {data_path}")
            else:
                logger.info(f"  {content}")

    except tomllib.TOMLDecodeError as e:
        logger.error(f"TOML Parse fail: {e}")
