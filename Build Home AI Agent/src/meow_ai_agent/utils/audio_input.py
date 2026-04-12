import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import torch
import queue
import threading
import time

# ================== 配置 ==================
MODEL_SIZE = r"models\faster-whisper-large-v3-turbo"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LANGUAGE = "zh"
SAMPLE_RATE = 16000

CHUNK_DURATION = 0.05  # 每50ms采集一次
MIN_SILENCE_MS = 800  # 停顿多久算一句结束
MIN_AUDIO_MS = 500  # 最短语音长度

# ================== 加载模型 ==================
print(f"加载 faster-whisper 模型（{DEVICE}）...")
model = WhisperModel(
    MODEL_SIZE,
    device=DEVICE,
    compute_type="float16" if DEVICE == "cuda" else "int8"
)

print("加载 VAD 模型...")
vad_model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False,
    onnx=True
)
(get_speech_timestamps, _, _, _, _) = utils

print("初始化完成")

# ================== 音频队列 ==================
audio_queue = queue.Queue()

# ================== 状态 ==================
current_buffer = []
is_speaking = False
last_speech_time = time.time()


# ================== 音频回调 ==================
def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy().flatten())


# ================== 主处理逻辑 ==================
def process_audio():
    global current_buffer, is_speaking, last_speech_time

    print("实时监听中（停顿自动转录）...\n")

    with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32',
            blocksize=int(SAMPLE_RATE * CHUNK_DURATION),
            callback=audio_callback
    ):
        while True:
            audio_chunk = audio_queue.get()
            current_buffer.extend(audio_chunk)

            # ====== 至少积累一点音频再做 VAD ======
            if len(current_buffer) < SAMPLE_RATE * 0.3:
                continue

            audio_array = np.array(current_buffer, dtype=np.float32)

            # ====== 只取最近 0.5 秒做 VAD ======
            recent_audio = audio_array[-int(SAMPLE_RATE * 0.5):]
            audio_tensor = torch.from_numpy(recent_audio)
            speech = get_speech_timestamps(
                audio_tensor,
                vad_model,
                sampling_rate=SAMPLE_RATE
            )

            now = time.time()

            if speech:
                if not is_speaking:
                    print("检测到说话...")
                is_speaking = True
                last_speech_time = now
            else:
                # ====== 判断是否结束一句话 ======
                if is_speaking and (now - last_speech_time) * 1000 > MIN_SILENCE_MS:
                    duration_ms = len(audio_array) / SAMPLE_RATE * 1000

                    if duration_ms > MIN_AUDIO_MS:
                        print("转录中...")

                        segments, _ = model.transcribe(
                            audio_array,
                            language=LANGUAGE,
                            vad_filter=True
                        )

                        text = "".join(seg.text for seg in segments).strip()

                        if text:
                            print(f"内容：{text}\n")

                    # ====== 重置状态 ======
                    current_buffer.clear()
                    is_speaking = False


# ================== 启动线程 ==================
threading.Thread(target=process_audio, daemon=True).start()

input("按回车键停止...\n")