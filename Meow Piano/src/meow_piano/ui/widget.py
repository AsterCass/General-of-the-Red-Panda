from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QDesktopServices

from meow_piano.constants.style import text_label_style, url_label_style, check_box_style, \
    text_label_style_piano_map_black, text_label_style_piano_map_white, text_label_style_piano_map_black_sp
from meow_piano.utils.resource import resource_path


class MainWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("喵喵钢琴")
        self.setWindowIcon(QIcon(resource_path("assets/logo.svg")))

        # 总布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(12)

        # 设置组件
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget {background-color: #f0f0f0;}")
        self.playPiano = QtWidgets.QCheckBox("钢琴律动")
        self.playPiano.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.playPiano.setStyleSheet(check_box_style)
        self.playPiano.toggled.connect(self._on_toggle_play_piano)
        self.playWave = QtWidgets.QCheckBox("屏幕律动")
        self.playWave.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.playWave.setStyleSheet(check_box_style)
        self.playWave.toggled.connect(self._on_toggle_play_wav)

        # 设置布局
        self.settingWidget = QtWidgets.QWidget()
        self.settingLayout = QtWidgets.QHBoxLayout(self.settingWidget)
        self.settingLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.settingLayout.addWidget(self.playPiano)
        self.settingLayout.addWidget(self.playWave)
        self.settingLayout.setContentsMargins(0, 0, 0, 0)
        self.settingLayout.setSpacing(4)
        self.layout.addWidget(self.settingWidget)

        # 键位提示
        self.keyBindLabel = QtWidgets.QLabel("钢琴律动键位绑定（Demo版本暂不支持修改）")
        self.keyBindLabel.setStyleSheet(text_label_style)
        self.layout.addWidget(self.keyBindLabel)

        # 键位内容
        self.allKeys = [
            ["1", "2", "4", "5", "6"],
            ["Tab", "Q", "W", "E", "R", "T", "Y"],
            ["A", "S", "D", "F", "G"],
            ["Caps", "Z", "X", "C", "V", "B", "H"],
            ["8", "9", "-", "=", "Back"],
            ["U", "I", "O", "P", "[", "]", "\\"],
            ["J", "K", "L", ";", "'"],
            ["Space", "N", "M", ",", ".", "/", "Enter"]
        ]
        self.baseBlackUP = ["C#", "D#", "F#", "G#", "A#"]
        self.baseWhiteUP = ["C", "D", "E", "F", "G", "A", "B"]
        self.allKeysLabel = []
        self.currentLeftBase = 2
        self.currentRightBase = 4
        # 渲染
        for i, row in enumerate(self.allKeys):
            rowLayout = QtWidgets.QHBoxLayout()
            rowLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            if i % 2 == 0:
                rowLayout.setContentsMargins(50, 0, 0, 0)
            else:
                rowLayout.setContentsMargins(0, 0, 0, 10)
            rowLayout.setSpacing(4)

            for j, key in enumerate(row):
                keyLabel = QtWidgets.QLabel()
                if i % 2 == 0:
                    if i <= 3:
                        keyLabel.setText(f"{key} --> {self.baseBlackUP[j]}{self.currentLeftBase + (i // 2)}")
                    else:
                        keyLabel.setText(f"{key} --> {self.baseBlackUP[j]}{self.currentRightBase + ((i - 4) // 2)}")
                    keyLabel.setStyleSheet(text_label_style_piano_map_black)
                    if j == 2:
                        keyLabel.setStyleSheet(text_label_style_piano_map_black_sp)
                else:
                    if i <= 3:
                        keyLabel.setText(f"{key} --> {self.baseWhiteUP[j]}{self.currentLeftBase + (i // 2)}")
                    else:
                        keyLabel.setText(f"{key} --> {self.baseWhiteUP[j]}{self.currentRightBase + ((i - 4) // 2)}")
                    keyLabel.setStyleSheet(text_label_style_piano_map_white)
                keyLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                rowLayout.addWidget(keyLabel)

            self.layout.addLayout(rowLayout)

        self.keysWidget1 = QtWidgets.QWidget()
        self.keysLayout1 = QtWidgets.QHBoxLayout(self.keysWidget1)
        self.keysLayout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.keysLayout1.setContentsMargins(0, 0, 0, 0)
        self.keysLayout1.setSpacing(4)

        # Copyright
        self.copyrightLabel = QtWidgets.QPushButton("版权所有：将军的鱿鱼炒面 AsterCasc")
        self.copyrightLabel.setStyleSheet(url_label_style)
        self.copyrightLabel.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.copyrightLabel.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.astercasc.com"))
        )
        self.layout.addWidget(self.copyrightLabel, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # 设置值
        self.playPiano.setChecked(True)
        self.playWave.setChecked(True)

    def _on_toggle_play_piano(self):
        # todo
        return

    def _on_toggle_play_wav(self):
        # todo
        return
