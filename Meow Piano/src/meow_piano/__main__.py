import sys

from PySide6 import QtWidgets

from meow_piano.config.logging import setup_logging
from meow_piano.constants.env import print_env
import meow_piano.constants.config as config
from meow_piano.ui.widget import MainWidget


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    print_env()
    config.load_config()
    # 初始化UI
    app = QtWidgets.QApplication([])
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
