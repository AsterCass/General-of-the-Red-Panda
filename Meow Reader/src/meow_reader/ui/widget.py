from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon
from loguru import logger

from meow_reader.constants.path import default_speak_model_path, default_trans_model_path
from meow_reader.constants.style import text_browser_style, text_label_style, push_btn_style, check_box_style
from meow_reader.utils.clipboard import ClipboardTextWatcher
from meow_reader.utils.reader import  Reader
from meow_reader.utils.translation import MarianTranslator


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵朗读")
        self.setWindowIcon(QIcon("assets/logo.svg"))
        self.resize(400, 600)

        # 设置组件
        self.onlyEnCheckBox = QtWidgets.QCheckBox("只处理纯英文")
        self.onlyEnCheckBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.onlyEnCheckBox.setStyleSheet(check_box_style)
        self.onlyEnCheckBox.toggled.connect(self._on_toggle_only_en)
        self.autoTrim = QtWidgets.QCheckBox("自动去掉首尾空格换行符等")
        self.autoTrim.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.autoTrim.setStyleSheet(check_box_style)
        self.autoTrim.toggled.connect(self._on_toggle_auto_trim)
        self.topMost = QtWidgets.QCheckBox("固定在顶端")
        self.topMost.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.topMost.setStyleSheet(check_box_style)
        self.topMost.toggled.connect(self._on_toggle_topmost)

        # 设置布局
        self.settingWidget = QtWidgets.QWidget()
        self.settingLayout = QtWidgets.QHBoxLayout(self.settingWidget)
        self.settingLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settingLayout.addWidget(self.onlyEnCheckBox)
        self.settingLayout.addWidget(self.autoTrim)
        self.settingLayout.addWidget(self.topMost)
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

        # 布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.settingWidget)
        self.layout.addWidget(self.textInputLabel)
        self.layout.addWidget(self.textInpout)
        self.layout.addWidget(self.textOutputLabel)
        self.layout.addWidget(self.textOutput)
        self.layout.addWidget(self.reReadBtn)
        self.layout.setSpacing(12)

        # 设置值
        self.onlyEnCheckBox.setChecked(True)
        self.autoTrim.setChecked(True)
        self.topMost.setChecked(True)

        # 监视剪贴板文本变化
        self.watcher = ClipboardTextWatcher()
        self.watcher.textChanged.connect(self._on_clipboard_text_changed)

        # 加载模型
        self.reader = Reader(default_speak_model_path)
        self.translator  = MarianTranslator(default_trans_model_path)

    def _on_clipboard_text_changed(self, text: str):
        self.textInpout.clear()
        self.textInpout.insertPlainText(text)
        ret = self.translator.translate(text)
        self.textOutput.clear()
        self.textOutput.setText(ret)
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

    def _on_toggle_only_en(self, checked: bool):
        logger.info(checked)

    def _on_toggle_auto_trim(self, checked: bool):
        logger.info(checked)
