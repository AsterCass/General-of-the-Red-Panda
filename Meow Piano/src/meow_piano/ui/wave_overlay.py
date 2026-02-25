import math
import random
import time

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, Slot

from meow_piano.utils.hotkey import PianoKeyboard


class Wave:
    def __init__(self, amplitude, ver_speed, color, width, hor_speed):
        self.amplitude = amplitude
        self.color = color
        self.width = width
        self.hor_speed = hor_speed
        self.ver_speed = ver_speed
        self.last_time = time.time()
        self.phase = 0

class WaveOverlay(QtWidgets.QWidget):
    # todo 支持自定义
    MAX_WAVES = 4
    MAX_HEIGHT = 100

    def __init__(self, piano: PianoKeyboard):
        super().__init__()
        self.piano = piano

        # 样式
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        #self.setStyleSheet("background-color: white")
        #self.resize(800, 600)

        screen = QtWidgets.QApplication.primaryScreen()
        self.setGeometry(screen.geometry())

        # 信号
        self.piano.keyPress.connect(self._on_key_press)

        # 波浪参数
        self.frequency = 0.02
        self.waves = []

        # 计时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)


    @Slot(bool, int)
    def _on_key_press(self, is_press, vk):
        if not is_press:
            return
        rng = random.Random(vk)
        color_int = rng.randint(0, 0xFFFFFF)
        r = (color_int >> 16) & 0xFF
        g = (color_int >> 8) & 0xFF
        b = color_int & 0xFF
        self.trigger(
            color=QtGui.QColor(r, g, b, 180),
            hor_speed=rng.uniform(0.2, 0.35),
            width=rng.randint(2, 5),
            ver_speed=rng.randint(15, 25),
            amplitude=rng.randint(30, 50),
        )
        return

    def trigger(self, amplitude=40, ver_speed=20, color=QtGui.QColor(0, 255, 255, 120), width=3, hor_speed=0.4):

        if len(self.waves) < self.MAX_WAVES:
            self.waves.append(Wave(amplitude, ver_speed, color, width, hor_speed))
            return

        update = min(self.waves, key=lambda w: w.amplitude)
        update.amplitude = min(update.amplitude + update.amplitude, self.MAX_HEIGHT)
        update.color = color
        update.width = width
        update.hor_speed = hor_speed

    def update_animation(self):
        now = time.time()
        alive_waves = []

        for wave in self.waves:
            dur = now - wave.last_time
            wave.last_time = now
            if wave.amplitude <= 1.0:
                continue
            wave.amplitude = wave.amplitude - dur * wave.ver_speed
            wave.phase += wave.hor_speed
            alive_waves.append(wave)

        self.waves = alive_waves
        self.update()


    def paintEvent(self, event):
        if not self.waves:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for wave in self.waves:
            pen = QtGui.QPen(wave.color)
            pen.setWidth(wave.width)
            painter.setPen(pen)
            self.draw_edges(painter, wave)

    def draw_edges(self, painter, wave):
        w = self.width()
        h = self.height()

        self.draw_horizontal_wave(painter, 0, True, wave)
        self.draw_horizontal_wave(painter, h, False, wave)
        self.draw_vertical_wave(painter, 0, True, wave)
        self.draw_vertical_wave(painter, w, False, wave)

    def draw_horizontal_wave(self, painter, y_base, top, wave):
        path = QtGui.QPainterPath()
        step = 8
        for x in range(0, self.width(), step):
            y = wave.amplitude * math.sin(x * self.frequency + wave.phase)
            if not top:
                y = -y
            final_y = y_base + y
            if x == 0:
                path.moveTo(x, final_y)
            else:
                path.lineTo(x, final_y)
        painter.drawPath(path)

    def draw_vertical_wave(self, painter, x_base, left, wave):
        path = QtGui.QPainterPath()
        step = 8
        for y in range(0, self.height(), step):
            x = wave.amplitude * math.sin(y * self.frequency + wave.phase)
            if not left:
                x = -x
            final_x = x_base + x
            if y == 0:
                path.moveTo(final_x, y)
            else:
                path.lineTo(final_x, y)
        painter.drawPath(path)
