import ctypes
import threading
from ctypes import wintypes

from PySide6.QtCore import QObject, Signal
from loguru import logger

from meow_piano.utils.audio import AudioEngine

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
HC_ACTION = 0

# =========================
# 只支持64位
# =========================

ULONG_PTR = ctypes.c_ulonglong
LRESULT = ctypes.c_longlong
HOOKPROC = ctypes.WINFUNCTYPE(
    LRESULT,
    ctypes.c_int,
    wintypes.WPARAM,
    wintypes.LPARAM
)


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# =========================
# 声明 WinAPI 签名（防止 Overflow）
# =========================

user32.SetWindowsHookExW.restype = wintypes.HHOOK
user32.SetWindowsHookExW.argtypes = (
    ctypes.c_int,
    HOOKPROC,
    wintypes.HINSTANCE,
    wintypes.DWORD,
)

user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = (
    wintypes.HHOOK,
    ctypes.c_int,
    wintypes.WPARAM,
    wintypes.LPARAM,
)

user32.UnhookWindowsHookEx.restype = wintypes.BOOL
user32.UnhookWindowsHookEx.argtypes = (wintypes.HHOOK,)

user32.GetMessageW.argtypes = (
    ctypes.POINTER(wintypes.MSG),
    wintypes.HWND,
    wintypes.UINT,
    wintypes.UINT,
)


# =========================
# Keyboard Hook 类
# https://www.xiwnn.com/piano/
# =========================

class KeyboardHook:
    def __init__(self, callback):
        self.callback = callback
        self.hook_id = None
        self.thread = None
        self.running = False
        self.hook_proc = None  # 防止被GC

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.hook_id:
            user32.UnhookWindowsHookEx(self.hook_id)
            self.hook_id = None

    def _run(self):
        self._install_hook()

        msg = wintypes.MSG()
        while self.running and user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def _install_hook(self):
        self.hook_proc = HOOKPROC(self._hook_callback)

        self.hook_id = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self.hook_proc,
            None,
            0
        )

        if not self.hook_id:
            logger.error(f"Hook Install fail {ctypes.GetLastError()}")
        else:
            logger.info("Hook Success")

    def _hook_callback(self, n_code, w_param, l_param):
        if n_code == HC_ACTION:
            kb = ctypes.cast(
                l_param,
                ctypes.POINTER(KBDLLHOOKSTRUCT)
            ).contents

            vk_code = kb.vkCode

            if w_param == WM_KEYDOWN:
                self.callback(vk_code, True)

            elif w_param == WM_KEYUP:
                self.callback(vk_code, False)

        return user32.CallNextHookEx(
            self.hook_id,
            n_code,
            w_param,
            l_param
        )


# =========================
# 实例律动逻辑
# =========================

def vk_to_string(vk):
    scan_code = user32.MapVirtualKeyW(vk, 0)
    lparam = (scan_code << 16)
    buffer = ctypes.create_unicode_buffer(32)
    user32.GetKeyNameTextW(lparam, buffer, 32)
    return buffer.value


# 初始键位和最低\高键位
LOWEST_START = 3
HIGHEST_START = 63
LEFT_START = 15
RIGHT_START = 39

# 基础映射
PIANO_BASE_LEFT_MAP = {
    9: 1,  # Tab
    49: 2,  # 1
    81: 3,  # Q
    50: 4,  # 2
    87: 5,  # W
    69: 6,  # E
    52: 7,  # 4
    82: 8,  # R
    53: 9,  # 5
    84: 10,  # T
    54: 11,  # 6
    89: 12,  # Y

    20: 12 + 1,  # Caps Lock
    90: 12 + 3,  # Z
    88: 12 + 5,  # X
    67: 12 + 6,  # C
    86: 12 + 8,  # V
    66: 12 + 10,  # B
    72: 12 + 12,  # H
    65: 12 + 2,  # A
    83: 12 + 4,  # S
    68: 12 + 7,  # D
    70: 12 + 9,  # F
    71: 12 + 11,  # G
}

PIANO_BASE_RIGHT_MAP = {
    85: 1,  # U
    56: 2,  # 8
    73: 3,  # I
    57: 4,  # 9
    79: 5,  # O
    80: 6,  # P
    189: 7,  # -
    219: 8,  # [
    187: 9,  # =
    221: 10,  # ]
    8: 11,  # Backspace
    220: 12,  # \

    32: 12 + 1,  # Space
    78: 12 + 3,  # N
    77: 12 + 5,  # M
    188: 12 + 6,  # ,
    190: 12 + 8,  # .
    191: 12 + 10,  # /
    13: 12 + 12,  # Enter
    74: 12 + 2,  # J
    75: 12 + 4,  # K
    76: 12 + 7,  # L
    186: 12 + 9,  # ;
    222: 12 + 11,  # '
}


class PianoKeyboard(QObject):
    keyPress = Signal(bool, int)
    keyPressWave = Signal(bool, int)
    octaveUpDown = Signal(bool ,bool)

    def __init__(self):
        super().__init__()
        self.audio_enable = True
        self.wave_enable = True
        self.octave_disable = False
        # 加载音频
        self.audio = AudioEngine("assets/wav")
        self.audio_velocity = 50
        # 键盘钩子
        self.hook = KeyboardHook(self._on_key)
        # 当前基础音调
        self.current_left_start = LEFT_START
        self.current_right_start = RIGHT_START
        # 长按不重复触发
        self.pressed_keys = set()

    def set_audio_velocity(self, value):
        self.audio_velocity = value

    def enable_audio(self, enable: bool):
        self.audio_enable = enable

    def enable_wave(self, enable: bool):
        self.wave_enable = enable

    def disable_octave(self, disable: bool):
        self.octave_disable = disable

    def _on_key(self, vk, is_down):
        if not is_down:
            self.pressed_keys.discard(vk)
            self.keyPress.emit(False, vk)
            return
        if vk in self.pressed_keys:
            return
        self.pressed_keys.add(vk)
        # 触发
        if self.wave_enable:
            self.keyPressWave.emit(True, vk)
        if not self.audio_enable:
            return
        self.keyPress.emit(True, vk)
        if vk == 160 and self.current_left_start < HIGHEST_START and (not self.octave_disable):  # Left Shift
            self.current_left_start = self.current_left_start + 12
            self.octaveUpDown.emit(True, False)
        if vk == 162 and self.current_left_start > LOWEST_START and (not self.octave_disable):  # Left Ctrl
            self.current_left_start = self.current_left_start - 12
            self.octaveUpDown.emit(True, True)
        if vk == 161 and self.current_right_start < HIGHEST_START and (not self.octave_disable):  # Right Shift
            self.current_right_start = self.current_right_start + 12
            self.octaveUpDown.emit(False, False)
        if vk == 163 and self.current_right_start > LOWEST_START and (not self.octave_disable):  # Right Ctrl
            self.current_right_start = self.current_right_start - 12
            self.octaveUpDown.emit(False, True)
        if vk in PIANO_BASE_LEFT_MAP:
            self.audio.note_on(PIANO_BASE_LEFT_MAP[vk] + self.current_left_start, self.audio_velocity)
        if vk in PIANO_BASE_RIGHT_MAP:
            self.audio.note_on(PIANO_BASE_RIGHT_MAP[vk] + self.current_right_start, self.audio_velocity)

    def start(self):
        self.hook.start()
