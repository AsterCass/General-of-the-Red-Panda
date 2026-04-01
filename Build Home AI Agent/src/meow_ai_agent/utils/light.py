from langchain.tools import tool
from loguru import logger


# todo 支持设置是否二次验证，以及其他属性

@tool
def turn_off_light_bedroom() -> str:
    """关闭卧室灯光"""
    logger.info("Turn off light 1...")
    return "卧室灯光已经关闭"


turn_off_light_bedroom.metadata = {
    "need_confirm": True,
    "category": "device"
}

@tool
def turn_off_light_living_room() -> str:
    """关闭客厅灯光"""
    logger.info("Turn off light 2...")
    return "客厅灯已经关闭"

@tool
def close_window_living_room() -> str:
    """关闭客厅窗户"""
    logger.info("Closing window...")
    return "客厅窗户已关闭"

@tool
def turn_on_heating_bedroom() -> str:
    """打开卧室暖气"""
    logger.info("Turn on heating...")
    return "卧室暖气已经打开"

