import re

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Slot, Signal, QUrl
from PySide6.QtGui import QIcon, QDesktopServices

import meow_reader.constants.config as config
from meow_reader.constants.style import text_browser_style, text_label_style, push_btn_style, check_box_style, \
    url_label_style
from meow_reader.utils.clipboard import ClipboardTextWatcher
from meow_reader.utils.reader import Reader
from meow_reader.utils.resource import resource_path
from meow_reader.utils.translation import MarianTranslator


class MainWidget(QtWidgets.QWidget):
    translation_done = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵朗读")
        self.setWindowIcon(QIcon(resource_path("assets/logo.svg")))
        self.resize(400, 600)
        # 记录上次文本
        self.last_text = ""

        # 设置组件
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget {background-color: #f0f0f0;}")
        self.onlyEnCheckBox = QtWidgets.QCheckBox("只处理纯英文")
        self.onlyEnCheckBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.onlyEnCheckBox.setStyleSheet(check_box_style)
        self.topMost = QtWidgets.QCheckBox("固定在顶端")
        self.topMost.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.topMost.setStyleSheet(check_box_style)
        self.topMost.toggled.connect(self._on_toggle_topmost)
        self.needMute = QtWidgets.QCheckBox("静音")
        self.needMute.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.needMute.setStyleSheet(check_box_style)

        # 设置布局
        self.settingWidget = QtWidgets.QWidget()
        self.settingLayout = QtWidgets.QHBoxLayout(self.settingWidget)
        self.settingLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settingLayout.addWidget(self.onlyEnCheckBox)
        self.settingLayout.addWidget(self.topMost)
        self.settingLayout.addWidget(self.needMute)
        self.settingLayout.setContentsMargins(0, 0, 0, 0)
        self.settingLayout.setSpacing(4)

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
        self.reReadBtn.clicked.connect(self._on_re_read)

        # Copyright
        self.copyrightLabel = QtWidgets.QPushButton("版权所有：将军的鱿鱼炒面 AsterCasc")
        self.copyrightLabel.setStyleSheet(url_label_style)
        self.copyrightLabel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.copyrightLabel.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.astercasc.com"))
        )

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.settingWidget)
        self.layout.addWidget(self.textInputLabel)
        self.layout.addWidget(self.textInpout)
        self.layout.addWidget(self.textOutputLabel)
        self.layout.addWidget(self.textOutput)
        self.layout.addWidget(self.reReadBtn)
        self.layout.addWidget(self.copyrightLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.layout.setSpacing(12)

        # 设置值
        self.onlyEnCheckBox.setChecked(True)
        self.topMost.setChecked(True)
        self.needMute.setChecked(False)

        # 信号
        self.translation_done.connect(self._update_text_input_output)

        # 监视剪贴板文本变化
        self.watcher = ClipboardTextWatcher()
        self.watcher.textChanged.connect(self._on_clipboard_text_changed)

        # 加载模型
        self.reader = Reader(config.speak_model_path)
        self.translator  = MarianTranslator(config.trans_model_path)

    @Slot(str, str)
    def _update_text_input_output(self, text: str, output: str):
        self.textInpout.clear()
        self.textInpout.insertPlainText(text)
        self.textOutput.clear()
        self.textOutput.setText(output)

    def _on_translated(self, text: str, output: str):
        self.translation_done.emit(text, output)

    def _on_clipboard_text_changed(self, text: str):
        if self.onlyEnCheckBox.isChecked() and not text.isascii():
            return
        text = re.sub(r'\s+', ' ', text).strip()
        if self.last_text == text:
            return
        self.last_text = text
        self.translator.translate(text, self._on_translated)
        if self.needMute.isChecked():
            return
        self.reader.speak(text)

    def _on_toggle_topmost(self, checked: bool):
        is_top = self.windowFlags() & QtCore.Qt.WindowType.WindowStaysOnTopHint
        if is_top and not checked:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, False)
            self.hide()
            self.show()
        elif not is_top and checked:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
            self.hide()
            self.show()

    @Slot()
    def _on_re_read(self):
        self.reader.speak(self.textInpout.toPlainText())
