from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QDesktopServices

from meow_piano.constants.style import text_browser_style, text_label_style, push_btn_style, check_box_style, \
    url_label_style
from meow_piano.utils.resource import resource_path


class MainWidget(QtWidgets.QWidget):

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

        # 设置布局
        self.settingWidget = QtWidgets.QWidget()
        self.settingLayout = QtWidgets.QHBoxLayout(self.settingWidget)
        self.settingLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settingLayout.addWidget(self.onlyEnCheckBox)
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
