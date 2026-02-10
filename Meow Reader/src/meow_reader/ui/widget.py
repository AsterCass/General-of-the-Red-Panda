from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon

from meow_reader.constants.style import text_browser_style, text_label_style, push_btn_style
from meow_reader.utils.clipboard import ClipboardTextWatcher
from meow_reader.utils.translation import set_model_dir, trans


# todo 选项 只处理纯英文 自动去掉首尾空格换行符 固定在最前端

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵朗读")
        self.setWindowIcon(QIcon("assets/logo.svg"))
        self.resize(400, 600)

        # 输入
        self.textInputLabel = QtWidgets.QLabel("剪贴板内容")
        self.textInputLabel.setStyleSheet(text_label_style)
        self.textInpout = QtWidgets.QTextBrowser()
        self.textInpout.contextMenuPolicy = QtCore.Qt.ContextMenuPolicy.NoContextMenu
        self.textInpout.setStyleSheet(text_browser_style)

        # 输出
        self.textOutputLabel = QtWidgets.QLabel("翻译")
        self.textOutputLabel.setStyleSheet(text_label_style)
        self.textOutput = QtWidgets.QTextBrowser()
        self.textOutput.contextMenuPolicy = QtCore.Qt.ContextMenuPolicy.NoContextMenu
        self.textOutput.setStyleSheet(text_browser_style)

        # 重复朗读
        self.reReadBtn = QtWidgets.QPushButton("再次朗读")
        self.reReadBtn.setStyleSheet(push_btn_style)

        # 置顶
        self.topMost = QtWidgets.QPushButton("置顶/取消置顶")
        self.topMost.setStyleSheet(push_btn_style)
        self.topMost.clicked.connect(self.toggle_topmost)

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.textInputLabel)
        self.layout.addWidget(self.textInpout)
        self.layout.addWidget(self.textOutputLabel)
        self.layout.addWidget(self.textOutput)
        self.layout.addWidget(self.reReadBtn)
        self.layout.addWidget(self.topMost)
        self.layout.setSpacing(12)

        # 监视剪贴板文本变化
        self.watcher = ClipboardTextWatcher()
        self.watcher.textChanged.connect(self._on_clipboard_text_changed)

        # 加载翻译模型
        set_model_dir()

    def _on_clipboard_text_changed(self, text: str):
        self.textInpout.clear()
        self.textInpout.insertPlainText(text)
        ret = trans(text)
        self.textOutput.clear()
        self.textOutput.setText(ret)

    def toggle_topmost(self):
        # 切换置顶状态
        is_top = self.windowFlags() & QtCore.Qt.WindowType.WindowStaysOnTopHint
        if is_top:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, False)
        else:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.hide()
        self.show()
