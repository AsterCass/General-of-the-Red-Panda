from PySide6.QtCore import QTimer, QObject, Signal
from PySide6.QtWidgets import QApplication


class ClipboardTextWatcher(QObject):
    """监视剪贴板文本变化的监视器"""
    textChanged = Signal(str)  # 当文本变化时发出信号

    def __init__(self, interval_ms=1000):
        super().__init__()
        self.clipboard = QApplication.clipboard()
        self.last_text = ""

        # 定时器轮询
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self._check_clipboard)
        self.timer.start()

    def _check_clipboard(self):
        try:
            current_text = self.clipboard.text().strip()
            # 只关心非空文本，且与上次不同
            if current_text and current_text != self.last_text:
                self.last_text = current_text
                self.textChanged.emit(current_text)

        except Exception:
            # 防止窗口关闭或剪贴板异常导致崩溃
            pass
