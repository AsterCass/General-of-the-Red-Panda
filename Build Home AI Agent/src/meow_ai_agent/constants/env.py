import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# services:
#   qdrant:
#     image: qdrant/qdrant
#     container_name: qdrant
#     restart: always
#     ports:
#       - "6333:6333"
#     volumes:
#       - ./data:/qdrant/storage
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
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
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b")
MODEL_NAME_LIGHT = os.getenv("MODEL_NAME_LIGHT", "qwen2.5:1.5b")
EMBED_TEXT_MODEL_NAME = os.getenv("EMBED_TEXT_MODEL_NAME", "bge-m3")
RESET_COLLECTIONS = os.getenv("RESET_COLLECTIONS", "false").lower() == "true"


APP_NAME = os.getenv("APP_NAME")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

def print_env():
    logger.info("Welcome {value}!", value=APP_NAME)
    logger.info("Current mode {value}!", value=DEV_MODE)