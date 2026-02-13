import tomllib
from pathlib import Path

from loguru import logger

trans_model_path = Path("models/opus-mt-en-zh")
speak_model_path = Path("models/en_US-lessac-medium/en_US-lessac-medium.onnx")
db_path = "models/dict/ecdict.db"


def load_config():
    path = Path("config.toml")
    global trans_model_path, speak_model_path, db_path

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
                    if k == "transModelPath":
                        trans_model_path = Path(v)
                        logger.info(f"Translation model path: {trans_model_path}")
                    if k == "speakModelPath":
                        speak_model_path = Path(v)
                        logger.info(f"Speak model path: {speak_model_path}")
                    if k == "dictDbPath":
                        logger.info(f"Dictionary DB path: {db_path}")
                        db_path = v
            else:
                logger.info(f"  {content}")

    except tomllib.TOMLDecodeError as e:
        logger.error(f"TOML Parse fail: {e}")
