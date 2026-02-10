import tkinter as tk

from meow_reader.config.logging import setup_logging
from meow_reader.constants.env import print_env, print_config
from PySide6 import QtWidgets
import sys

from meow_reader.ui.widget import MainWidget


def main():
    """程序主入口"""
    # 基础配置
    setup_logging(False)
    print_env()
    print_config()
    # 初始化UI
    app = QtWidgets.QApplication([])
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
