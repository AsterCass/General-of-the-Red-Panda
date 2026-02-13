from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from meow_reader.constants.style import splash_window_style
from meow_reader.utils.resource import resource_path


class SplashWindow(QWidget):
    """
    启动页面，暂时不需要
    """

    def __init__(self):
        super().__init__()
        # 基础背景
        self.setWindowIcon(QIcon(resource_path("assets/logo.svg")))
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(240, 80)

        # 内容
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setGeometry(0, 0, 240, 80)

        self.logo = QSvgWidget(resource_path("assets/logo.svg"))
        self.logo.setFixedSize(25, 25)

        self.label = QLabel("正在加载模型中，请稍等")
        self.container.setStyleSheet(splash_window_style)

        # 布局
        self.layout = QHBoxLayout(self.container)
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 动画
        self.dots = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dots)
        self.timer.start(500)

    def update_dots(self):
        self.dots = (self.dots + 1) % 4
        self.label.setText("正在加载模型中，请稍等" + "." * self.dots)

    @Slot()
    def close_splash(self):
        self.close()
