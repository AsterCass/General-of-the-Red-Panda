import sys

from PySide6 import QtWidgets

import meow_piano.constants.config as config
from meow_piano.config.logging import setup_logging
from meow_piano.constants.env import print_env
from meow_piano.ui.wave_overlay import WaveOverlay
from meow_piano.ui.widget import MainWidget
from meow_piano.utils.hotkey import PianoKeyboard


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    print_env()
    config.load_config()
    # 热键注册
    piano = PianoKeyboard()
    piano.start()
    # 初始化UI
    app = QtWidgets.QApplication([])
    widget = MainWidget(piano)
    widget.show()
    # 波浪窗口
    overlay = WaveOverlay(piano)
    overlay.show()
    # 程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
