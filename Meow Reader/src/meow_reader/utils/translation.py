import threading
from pathlib import Path

import torch
from loguru import logger
from transformers import MarianMTModel, MarianTokenizer

from meow_reader.constants.path import db_path
from meow_reader.utils.sqlite import query_dict


class MarianTranslator:
    """
    # 翻译模型 https://www.modelscope.cn/organization/Helsinki-NLP?tab=model
    # 翻译模型 https://huggingface.co/Helsinki-NLP/models
    # 字典 https://github.com/skywind3000/ECDICT
    """

    def __init__(self, model_dir: Path, device: str = None):
        if not model_dir.is_dir():
            raise FileNotFoundError(f"模型目录不存在: {model_dir}")

        if not (model_dir / "config.json").is_file():
            raise FileNotFoundError(f"缺少 config.json: {model_dir}")

        # 自动设备选择
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加载模型
        try:
            self.tokenizer = MarianTokenizer.from_pretrained(
                model_dir,
                local_files_only=True,
            )

            self.model = MarianMTModel.from_pretrained(
                model_dir,
                local_files_only=True,
            )

            self.model.to(self.device)
            self.model.eval()

            logger.info(
                f"翻译模型加载成功：{model_dir.name} | 设备: {self.device}"
            )
        except Exception as e:
            raise RuntimeError(f"加载模型失败: {e}")

    def _translate_in_thread(self, text, cb):
        if " " not in text and len(text.split()) == 1:
            translated_text = query_dict(db_path, text)
            if translated_text:
                cb(text, translated_text)
                return
        # 纠正单字符翻译问题
        prompt = f"This is a test: {text}."
        tokens = self.tokenizer(prompt, return_tensors="pt", padding=True)
        translated = self.model.generate(**tokens)
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        cb(text, translated_text.split(':', 1)[-1].strip() if ':' in translated_text else translated_text.strip())

    def translate(self, text: str, cb):
        threading.Thread(target=self._translate_in_thread, args=(text, cb)).start()
