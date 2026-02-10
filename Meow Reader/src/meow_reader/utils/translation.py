from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
from loguru import logger


class MarianTranslator:
    """
    # https://www.modelscope.cn/organization/Helsinki-NLP?tab=model
    # https://huggingface.co/Helsinki-NLP/models
    MarianMT 离线翻译器封装类（基于 Opus-MT 模型）
    """

    def __init__(self, model_dir: Path):
        """
        初始化翻译器，加载本地模型和 tokenizer
        """
        self.model_dir = model_dir

        if not self.model_dir.is_dir():
            raise FileNotFoundError(f"模型目录不存在或不是文件夹: {self.model_dir}")

        if not (self.model_dir / "config.json").is_file():
            raise FileNotFoundError(f"缺少 config.json 文件: {self.model_dir}")

        try:
            # 强制本地加载，禁止任何网络请求
            self.tokenizer = MarianTokenizer.from_pretrained(
                self.model_dir,
                local_files_only=True,
            )

            self.model = MarianMTModel.from_pretrained(
                self.model_dir,
                local_files_only=True,
            )

            # 把模型移到 GPU
            # self.model = self.model.to("cuda") if torch.cuda.is_available() else self.model

            logger.info(f"MarianMT 模型加载成功：{self.model_dir.name}")

        except Exception as e:
            raise RuntimeError(f"加载 MarianMT 模型失败: {e}\n请检查模型文件是否完整")

    def translate(
            self,
            text: str,
    ) -> str:
        """
        执行翻译
        """
        tokens = self.tokenizer(text, return_tensors="pt", padding=True)
        translated = self.model.generate(**tokens)
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text


loaded_model = False
current_model_dir = Path("models\opus-mt-en-zh")
translator: MarianTranslator


def trans(text: str) -> str:
    global translator
    global loaded_model
    if not loaded_model:
        # 加载模型
        translator = MarianTranslator(
            model_dir=current_model_dir
        )
        loaded_model = True
    return translator.translate(text)


def set_model_dir(model_dir: Path = current_model_dir):
    global translator
    global loaded_model
    global current_model_dir
    current_model_dir = model_dir
    translator = MarianTranslator(
        model_dir=model_dir
    )
    loaded_model = True
