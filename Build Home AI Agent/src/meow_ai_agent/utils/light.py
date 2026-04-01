from langchain.tools import tool
from loguru import logger

@tool
def turn_off_light_1() -> str:
    """关闭卧室灯光"""
    logger.info("Turn off light 1...")
    return "卧室灯光已经关闭"

@tool
def turn_off_light_2() -> str:
    """关闭客厅灯光"""
    logger.info("Turn off light 2...")
    return "客厅灯已经关闭"

@tool
def close_window() -> str:
    """关闭客厅窗户"""
    logger.info("Closing window...")
    return "客厅窗户已关闭"

@tool
def turn_on_heating() -> str:
    """打开卧室暖气"""
    logger.info("Turn on heating...")
    return "卧室暖气已经打开"

