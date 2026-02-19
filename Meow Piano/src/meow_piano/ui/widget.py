from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QDesktopServices

from meow_piano.constants.style import text_label_style, push_btn_style, url_label_style
from meow_piano.utils.resource import resource_path


class MainWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵钢琴")
        self.setWindowIcon(QIcon(resource_path("assets/logo.svg")))
        self.resize(400, 300)

        # 设置组件
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget {background-color: #f0f0f0;}")

        # 键位提示
        self.keyBindLabel = QtWidgets.QLabel("键位绑定（DEMO版本暂不支持修改）")
        self.keyBindLabel.setStyleSheet(text_label_style)

        # 键位内容


        # 重复朗读
        self.reReadBtn = QtWidgets.QPushButton("开始")
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
        self.layout.addWidget(self.keyBindLabel)
        self.layout.addWidget(self.reReadBtn)
        self.layout.addWidget(self.copyrightLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.layout.setSpacing(12)



    # https://www.xiwnn.com/piano/
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        key_map = {
            QtCore.Qt.Key.Key_J: "39",
        }

