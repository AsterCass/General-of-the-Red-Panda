import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import sounddevice as sd
import torch
from faster_whisper import WhisperModel
from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.constants.enums import AudioProcessorState


# ================== 配置数据类 ==================
@dataclass
class AudioConfig:
    """音频处理配置"""
    model: str
    vad: str
    language: str
    sample_rate: int
    chunk_duration: float
    min_silence_ms: int
    min_audio_ms: int
    vad_window_sec: float
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type: str = None

    def __post_init__(self):
        if self.compute_type is None:
            self.compute_type = "float16" if self.device == "cuda" else "int8"


# ================== 音频处理器 ==================
class AudioProcessor:
    """
    实时音频处理器：
    - 监听麦克风输入
    - 使用VAD检测语音
    - 使用Faster-Whisper进行语音识别
    - 支持流式转录回调
    """

    def __init__(
            self,
            config: Optional[AudioConfig] = None,
            on_text_callback: Optional[Callable[[str], None]] = None,
            on_partial_callback: Optional[Callable[[str], None]] = None
    ):
        """
        初始化音频处理器

        Args:
            config: 音频配置
            on_text_callback: 完整文本回调函数 fn(text: str)
            on_partial_callback: 部分文本回调函数（实时显示）fn(partial_text: str)
        """
        self.config = config
        self.on_text_callback = on_text_callback
        self.on_partial_callback = on_partial_callback
        self.state = AudioProcessorState.IDLE
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

        # 音频缓冲
        self.current_buffer = np.zeros(0, dtype=np.float32)
        self.is_speaking = False
        self.last_speech_time = time.time()

        # 队列限制队列大小防止内存溢出
        self.audio_queue = queue.Queue(maxsize=50)

        # 线程池用于异步转录
        self._executor = ThreadPoolExecutor(max_workers=1)

        logger.info(f"初始化音频处理器 (设备: {self.config.device})")
        self._load_models()

    def _load_models(self):
        """加载Whisper和VAD模型"""
        try:
            logger.info(f"加载 Faster-Whisper 模型 ({self.config.device})...")
            self.whisper_model = WhisperModel(
                self.config.model,
                device=self.config.device,
                compute_type=self.config.compute_type
            )

            logger.info("加载 Silero VAD 模型...")
            vad_model, utils = torch.hub.load(
                repo_or_dir=self.config.vad,
                model='silero_vad',
                source='local',
                force_reload=False,
                onnx=True
            )
            self.vad_model = vad_model
            (self.get_speech_timestamps, _, _, _, _) = utils

            logger.info("模型加载完成")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise

    def _audio_callback(self, indata, frames, time_info, status):
        """音频输入回调"""
        if status:
            logger.warning(f"音频回调状态: {status}")
        if config.audio_is_playing:
            return
        try:
            # 更高效的方式：直接转换为numpy数组
            audio_chunk = indata[:, 0].astype(np.float32)
            self.audio_queue.put_nowait(audio_chunk)
        except queue.Full:
            logger.warning("音频队列满，丢弃数据")

    def _detect_speech(self, audio_array: np.ndarray) -> bool:
        """使用VAD检测是否有语音"""
        try:
            # 只取最近的音频做VAD检测
            vad_window_samples = int(self.config.sample_rate * self.config.vad_window_sec)
            recent_audio = audio_array[-vad_window_samples:]

            audio_tensor = torch.from_numpy(recent_audio)
            speech_timestamps = self.get_speech_timestamps(
                audio_tensor,
                self.vad_model,
                sampling_rate=self.config.sample_rate
            )
            return bool(speech_timestamps)
        except Exception as e:
            logger.error(f"VAD检测失败: {e}")
            return False

    def _transcribe_audio(self, audio_array: np.ndarray) -> str:
        """转录音频"""
        try:
            logger.info("转录中...")
            segments, _ = self.whisper_model.transcribe(
                audio_array,
                language=self.config.language,
                vad_filter=True
            )
            text = "".join(seg.text for seg in segments).strip()
            return text
        except Exception as e:
            logger.error(f"转录失败: {e}")
            return ""

    def _process_audio_stream(self):
        """主处理循环"""
        logger.info("实时监听中（停顿自动转录）...\n")

        chunk_size = int(self.config.sample_rate * self.config.chunk_duration)
        min_buffer_size = int(self.config.sample_rate * 0.3)
        min_buffer_samples = int(self.config.sample_rate * (self.config.min_audio_ms / 1000))
        max_buffer_samples = int(self.config.sample_rate * 30)  # 防止缓冲区过大

        self.state = AudioProcessorState.LISTENING

        with sd.InputStream(
                samplerate=self.config.sample_rate,
                channels=1,
                dtype='float32',
                blocksize=chunk_size,
                callback=self._audio_callback
        ):
            while not self._stop_event.is_set():
                try:

                    if config.audio_is_playing:
                        self.current_buffer = np.zeros(0, dtype=np.float32)
                        time.sleep(0.5)
                        continue

                    # 获取音频块，超时防止无限等待
                    audio_chunk = self.audio_queue.get(timeout=0.5)

                    with self._lock:
                        self.current_buffer = np.concatenate([self.current_buffer, audio_chunk])

                        # 防止缓冲区过大
                        if len(self.current_buffer) > max_buffer_samples:
                            self.current_buffer = self.current_buffer[-max_buffer_samples:]

                        # 至少积累一点音频再做VAD
                        if len(self.current_buffer) < min_buffer_size:
                            continue

                        # 检测语音
                        is_speech = self._detect_speech(self.current_buffer)
                        now = time.time()

                        if is_speech:
                            if not self.is_speaking:
                                logger.info("检测到说话...")
                            self.is_speaking = True
                            self.last_speech_time = now
                        else:
                            # 判断是否结束一句话
                            silence_duration = (now - self.last_speech_time) * 1000
                            if self.is_speaking and silence_duration > self.config.min_silence_ms:
                                buffer_duration = len(self.current_buffer) / self.config.sample_rate * 1000

                                if len(self.current_buffer) > min_buffer_samples:
                                    self.state = AudioProcessorState.PROCESSING

                                    # 使用线程池异步转录
                                    future = self._executor.submit(self._transcribe_audio, self.current_buffer.copy())
                                    text = future.result()

                                    self.state = AudioProcessorState.LISTENING

                                    if text:
                                        logger.info(f"识别内容: {text}")
                                        # 调用完整文本回调
                                        if self.on_text_callback:
                                            self.on_text_callback(text)
                                        # 调用部分文本回调（用于实时显示）
                                        if self.on_partial_callback:
                                            self.on_partial_callback(text)

                                # 重置状态
                                self.current_buffer = np.zeros(0, dtype=np.float32)
                                self.is_speaking = False

                except queue.Empty:
                    # 超时，继续循环
                    continue
                except Exception as e:
                    logger.error(f"处理音频时出错: {e}")
                    continue

        self.state = AudioProcessorState.STOPPED
        logger.info("音频处理已停止")

    def start(self):
        """启动音频处理（后台线程）"""
        if self.state != AudioProcessorState.IDLE:
            logger.warning("音频处理器已启动")
            return

        self._stop_event.clear()
        thread = threading.Thread(target=self._process_audio_stream, daemon=True)
        thread.start()
        return thread

    def stop(self):
        """停止音频处理"""
        logger.info("停止音频处理...")
        self._stop_event.set()
        self._executor.shutdown(wait=True)

    def is_running(self) -> bool:
        """检查是否正在运行"""
        return self.state in [AudioProcessorState.LISTENING, AudioProcessorState.PROCESSING]


# ================== 工厂函数 ==================
def create_audio_processor(
        model: str,
        vad: str,
        language,
        sample_rate,
        chunk_duration,
        min_silence_ms,
        min_audio_ms,
        vad_window_sec,
        on_text_callback: Optional[Callable[[str], None]] = None,
        on_partial_callback: Optional[Callable[[str], None]] = None
) -> AudioProcessor:
    """
    创建音频处理器的工厂函数

    Args:
        model: 模型路径
        vad: 语音活动检测
        language: 识别语言
        sample_rate: 采样率
        chunk_duration: 每个音频块的时长
        min_silence_ms: 最小静音时长
        min_audio_ms: 最小音频长度
        vad_window_sec: VAD窗口大小
        on_text_callback: 完整文本回调
        on_partial_callback: 部分文本回调

    Returns:
        AudioProcessor: 配置好的音频处理器
    """
    config = AudioConfig(
        model=model,
        vad=vad,
        language=language,
        sample_rate=sample_rate,
        chunk_duration=chunk_duration,
        min_silence_ms=min_silence_ms,
        min_audio_ms=min_audio_ms,
        vad_window_sec=vad_window_sec
    )
    return AudioProcessor(
        config=config,
        on_text_callback=on_text_callback,
        on_partial_callback=on_partial_callback
    )
