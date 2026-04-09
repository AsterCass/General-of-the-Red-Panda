import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

QDRANT_URL = "http://localhost:6333"
# services:
#   ollama:
#     image: qdrant/qdrant
#     container_name: qdrant
#     restart: always
#     ports:
#       - "6333:6333"
#     volumes:
#       - ./data:/qdrant/storage
OLLAMA_BASE_URL = "http://localhost:11434"
# services:
#   ollama:
#     image: ollama/ollama
#     container_name: ollama
#     restart: always
#     ports:
#       - "11434:11434"
#     volumes:
#       - ./data:/root/.ollama
#
# ollama pull qwen2.5:7b
# ollama pull nomic-embed-text
# ollama pull qwen2.5:1.5b
# ollama pull bge-m3
REDIS_URL = "redis://localhost:6379"
MODEL_NAME = "qwen2.5:7b"
MODEL_NAME_LIGHT = "qwen2.5:1.5b"
EMBED_TEXT_MODEL_NAME = "bge-m3"

def get_app_name():
    return os.getenv("APP_NAME")

def get_is_dev() -> bool:
    return os.getenv("DEV_MODE", "false").lower() == "true"

def print_env():
    APP_NAME = os.getenv("APP_NAME")
    DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

    logger.info("Welcome {value}!", value=APP_NAME)
    logger.info("Current mode {value}!", value=DEV_MODE)