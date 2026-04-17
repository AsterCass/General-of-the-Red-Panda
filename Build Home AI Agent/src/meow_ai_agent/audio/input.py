import queue
import threading
import time
from typing import Callable, Optional

import numpy as np
import sounddevice as sd
import torch
from faster_whisper import WhisperModel
from loguru import logger

import meow_ai_agent.constants.config as config
from meow_ai_agent.constants.enums import AudioProcessorState


class AudioInput:
    """
    实时音频处理器：
    - 监听麦克风输入
    - 使用VAD检测语音
    - 语音识别
    """

    def __init__(self, on_text_callback: Optional[Callable[[str], None]]):
        """
        初始化音频处理器
        """
        # config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        self.model = config.audio_settings.model
        self.vad = config.audio_settings.vad
        self.language = config.audio_settings.language
        self.sample_rate = config.audio_settings.sample_rate
        self.chunk_duration = config.audio_settings.chunk_duration
        self.min_silence_ms = config.audio_settings.min_silence_ms
        self.min_audio_ms = config.audio_settings.min_audio_ms
        self.vad_window_sec = config.audio_settings.vad_window_sec
        # extra
        self.on_text_callback = on_text_callback
        self.state = AudioProcessorState.IDLE
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        self.is_paused = False

        # 音频缓冲
        self.current_buffer = np.zeros(0, dtype=np.float32)
        self.is_speaking = False
        self.last_speech_time = time.time()

        # 队列限制队列大小防止内存溢出
        self.audio_queue = queue.Queue(maxsize=200)

        logger.info(f"初始化音频处理器 (设备: {self.device})")
        self._load_models()

    def _load_models(self):
        """加载Whisper和VAD模型"""
        try:
            logger.info(f"加载 Faster-Whisper 模型 ({self.device})...")
            self.whisper_model = WhisperModel(
                self.model,
                device=self.device,
                compute_type=self.compute_type
            )

            logger.info("加载 Silero VAD 模型...")
            vad_model, utils = torch.hub.load(
                repo_or_dir=self.vad,
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
        if self.is_paused:
            return
        try:
            audio_chunk = indata[:, 0].astype(np.float32)
            self.audio_queue.put_nowait(audio_chunk)
        except queue.Full:
            logger.warning("音频队列满，丢弃数据")


    def _detect_speech(self, audio_array: np.ndarray) -> bool:
        """使用VAD检测是否有语音"""
        try:
            # 只取最近的音频做VAD检测
            vad_window_samples = int(self.sample_rate * self.vad_window_sec)
            recent_audio = audio_array[-vad_window_samples:]

            audio_tensor = torch.from_numpy(recent_audio)
            speech_timestamps = self.get_speech_timestamps(
                audio_tensor,
                self.vad_model,
                sampling_rate=self.sample_rate
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
                language=self.language,
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

        chunk_size = int(self.sample_rate * self.chunk_duration)
        min_buffer_size = int(self.sample_rate * 0.3)
        min_buffer_samples = int(self.sample_rate * (self.min_audio_ms / 1000))
        max_buffer_samples = int(self.sample_rate * 30)  # 防止缓冲区过大

        self.state = AudioProcessorState.LISTENING

        with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                blocksize=chunk_size,
                callback=self._audio_callback
        ):
            while not self._stop_event.is_set():
                try:
                    # 获取音频块
                    audio_chunk = self.audio_queue.get()

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
                            if self.is_speaking and silence_duration > self.min_silence_ms:
                                # buffer_duration = len(self.current_buffer) / self.sample_rate * 1000

                                if len(self.current_buffer) > min_buffer_samples:
                                    self.state = AudioProcessorState.PROCESSING

                                    # 同步转录
                                    text = self._transcribe_audio(self.current_buffer.copy())

                                    self.state = AudioProcessorState.LISTENING

                                    if text:
                                        logger.info(f"识别内容: {text}")
                                        # 调用完整文本回调
                                        if self.on_text_callback:
                                            self.on_text_callback(text)
                                    else:
                                        logger.info("未识别到有效文本")

                                # 重置状态
                                self.current_buffer = np.zeros(0, dtype=np.float32)
                                self.is_speaking = False
                except Exception as e:
                    logger.error(f"处理音频时出错: {e}")
                    continue

        self.state = AudioProcessorState.STOPPED
        logger.info("音频处理已停止")

    def start(self):
        """启动音频处理（阻塞式）"""
        if self.state != AudioProcessorState.IDLE:
            logger.warning("音频处理器已启动")
            return

        self._stop_event.clear()
        self._process_audio_stream()

    def stop(self):
        """停止音频处理"""
        logger.info("停止音频处理...")
        self._stop_event.set()

    def is_running(self) -> bool:
        """检查是否正在运行"""
        return self.state in [AudioProcessorState.LISTENING, AudioProcessorState.PROCESSING]

    def pause(self):
        logger.info("暂停监听...")
        self.is_paused = True
        with self._lock:
            self.clear_queue()
            self.current_buffer = np.zeros(0, dtype=np.float32)
            self.is_speaking = False

    def resume(self):
        """恢复监听"""
        logger.info("恢复监听...")
        with self._lock:
            self.is_paused = False
            self.last_speech_time = time.time()

    def clear_queue(self):
        """清空音频队列"""
        cleared_count = 0
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
                cleared_count += 1
            except queue.Empty:
                break
        if cleared_count > 0:
            logger.debug(f"已清空音频队列中的 {cleared_count} 个块")
