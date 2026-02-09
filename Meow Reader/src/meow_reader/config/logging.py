# logging_config.py
from loguru import logger
import sys
from pathlib import Path

def setup_logging(save_file: bool = True):
    logger.remove()

    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name: <20}</cyan> | <level>{message}</level>",
        colorize=True,
    )

    if save_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        logger.add(
            log_dir / "app_{time:YYYY-MM-DD}.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
            compression="zip",
            encoding="utf-8",
        )