from meow_reader.config.logging import setup_logging
from meow_reader.constants.env import print_env, print_config


def main():
    """程序主入口"""
    setup_logging(False)
    print_env()
    print_config()


if __name__ == "__main__":
    main()
