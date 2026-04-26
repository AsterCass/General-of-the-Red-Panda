import tomllib
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

# 默认数据库路径
data_path = "data/data.db"

# 输入模式配置 "text" 或 "audio"
input_mode = "text"

# 输出模式配置 "text" 或 "audio"
output_mode = "text"

# 输出模式为 audio 需要加载的语言的模型
speak_model_path = "models/zh_CN-xiao_ya-medium/zh_CN-xiao_ya-medium.onnx"

# 是否为半双工对话，默认回声消除由硬件侧处理，如果硬件侧没有处理则参考 tests/ace.py 改写相关代码，如果都不处理则将改值置为 False
half_duplex_communication = True

@dataclass
class AudioSettings:
    """音频配置数据类"""
    model: str = "models/faster-whisper-large-v3-turbo"
    vad: str = "models/silero-vad"
    language: str = "zh"
    sample_rate: int = 16000
    chunk_duration: float = 0.05
    min_silence_ms: int = 800
    min_audio_ms: int = 500
    vad_window_sec: float = 0.5


audio_settings = AudioSettings()


# services:
#   redis:
#     image: redis/redis-stack:latest
#     container_name: redis
#     restart: always
#     ports:
#       - "6379:6379"
#     volumes:
#       - ./data:/data
# services:
#   qdrant:
#     image: qdrant/qdrant
#     container_name: qdrant
#     restart: always
#     ports:
#       - "6333:6333"
#     volumes:
#       - ./data:/qdrant/storage
#
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

@dataclass
class ServiceSettings:
    """服务配置数据类"""
    qdrant_url: str = "http://localhost:6333"
    ollama_base_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379"
    llm_model: str = "qwen2.5:7b"
    llm_model_light: str = "qwen2.5:1.5b"
    embed_text_model: str = "bge-m3"
    reset_collections: bool = False


service_settings = ServiceSettings()

def load_config():
    path = Path("config.toml")
    global data_path, input_mode, audio_settings, \
        service_settings, output_mode, speak_model_path, half_duplex_communication

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
                    elif section == "input" and k == "mode":
                        input_mode = v
                    elif section == "input" and k == "half_duplex_communication":
                        half_duplex_communication = v.lower() == "true"
                    elif section == "output" and k == "mode":
                        output_mode = v
                    elif section == "speaker" and k == "model":
                        speak_model_path = v
                    elif section == "audio":
                        if hasattr(audio_settings, k):
                            setattr(audio_settings, k, v)
                    elif section == "service":
                        if hasattr(service_settings, k):
                            setattr(service_settings, k, v)
            else:
                logger.info(f"  {content}")

    except tomllib.TOMLDecodeError as e:
        logger.error(f"TOML Parse fail: {e}")
