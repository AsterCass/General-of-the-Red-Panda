import math

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, Slot

from meow_piano.constants.style import text_label_style_desc
from meow_piano.utils.hotkey import PianoKeyboard


class WaveOverlay(QtWidgets.QWidget):
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
        self.phase = 0.0
        self.amplitude = 0.0
        self.target_amplitude = 0.0
        self.frequency = 0.02
        self.speed = 0.15
        self.line_width = 3

        # 计时器（60FPS）
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(16)



    @Slot(bool, int)
    def _on_key_press(self, is_press, vk):
        if not is_press:
            return
        self.trigger()
        return


    def trigger(self, strength=1.0):
        self.target_amplitude += 20 * strength
        self.target_amplitude = min(self.target_amplitude, 80)

    def _update_animation(self):
        # 平滑振幅衰减（阻尼）
        self.amplitude += (self.target_amplitude - self.amplitude) * 0.15
        self.target_amplitude *= 0.92
        # 相位推进
        self.phase += self.speed
        self.update()


    def paintEvent(self, event):
        if self.amplitude < 0.5:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(0, 255, 180, 200))
        pen.setWidth(self.line_width)
        painter.setPen(pen)

        w = self.width()
        h = self.height()

        self._draw_horizontal_wave(painter, 0, True)
        self._draw_horizontal_wave(painter, h, False)
        self._draw_vertical_wave(painter, 0, True)
        self._draw_vertical_wave(painter, w, False)


    def _draw_horizontal_wave(self, painter, y_base, top=True):
        path = QtGui.QPainterPath()
        step = 8

        for x in range(0, self.width(), step):
            y = self.amplitude * math.sin(x * self.frequency + self.phase)
            if not top:
                y = -y

            final_y = y_base + y

            if x == 0:
                path.moveTo(x, final_y)
            else:
                path.lineTo(x, final_y)

        painter.drawPath(path)


    def _draw_vertical_wave(self, painter, x_base, left=True):
        path = QtGui.QPainterPath()
        step = 8

        for y in range(0, self.height(), step):
            x = self.amplitude * math.sin(y * self.frequency + self.phase)
            if not left:
                x = -x

            final_x = x_base + x

            if y == 0:
                path.moveTo(final_x, y)
            else:
                path.lineTo(final_x, y)

        painter.drawPath(path)