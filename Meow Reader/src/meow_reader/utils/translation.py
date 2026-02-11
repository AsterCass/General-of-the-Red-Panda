from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
from loguru import logger
import torch
import threading


class MarianTranslator:
    """
    # https://www.modelscope.cn/organization/Helsinki-NLP?tab=model
    # https://huggingface.co/Helsinki-NLP/models
    """

    def __init__(self, model_dir: Path, device: str = None):
        if not model_dir.is_dir():
            raise FileNotFoundError(f"模型目录不存在: {model_dir}")

        if not (model_dir / "config.json").is_file():
            raise FileNotFoundError(f"缺少 config.json: {model_dir}")

        self._lock = threading.Lock()
        self.model_dir = model_dir

        # 自动设备选择
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self._load_model()


    def _load_model(self):
        try:
            self.tokenizer = MarianTokenizer.from_pretrained(
                self.model_dir,
                local_files_only=True,
            )

            self.model = MarianMTModel.from_pretrained(
                self.model_dir,
                local_files_only=True,
            )

            self.model.to(self.device)
            self.model.eval()

            logger.info(
                f"翻译模型加载成功：{self.model_dir.name} | 设备: {self.device}"
            )

        except Exception as e:
            raise RuntimeError(f"加载模型失败: {e}")


    def translate(
        self,
        text: str,
    ) -> str:

        if not text.strip():
            return ""

        with self._lock:
            with torch.no_grad():
                tokens = self.tokenizer(text, return_tensors="pt", padding=True)
                translated = self.model.generate(**tokens)
                translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
                return translated_text

