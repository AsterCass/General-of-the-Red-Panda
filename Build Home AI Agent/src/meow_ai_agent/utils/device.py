from langchain.tools import tool
from loguru import logger

def smart_tool(**meta):
    def wrapper(func):
        t = tool(func)
        t.metadata = meta
        return t

    return wrapper


@smart_tool(need_confirm=True, category="device")
def turn_off_light_bedroom() -> str:
    """关闭卧室灯光"""
    logger.info("Turn off light 1...")
    return "卧室灯光已关闭"


@smart_tool(need_confirm=True, category="device")
def turn_off_light_living_room() -> str:
    """关闭客厅灯光"""
    logger.info("Turn off light 2...")
    return "客厅灯光已关闭"


@smart_tool(need_confirm=True, category="device")
def close_window_living_room() -> str:
    """关闭客厅窗户"""
    logger.info("Closing window...")
    return "客厅窗户已关闭"


@smart_tool(need_confirm=True, category="device")
def turn_on_heating_bedroom() -> str:
    """打开卧室暖气"""
    logger.info("Turn on heating...")
    return "卧室暖气已打开"


@smart_tool(need_confirm=False, category="device")
def open_curtain_living_room() -> str:
    """打开客厅窗帘"""
    logger.info("Open curtain living room...")
    return "客厅窗帘已打开"


@smart_tool(need_confirm=False, category="device")
def close_curtain_living_room() -> str:
    """关闭客厅窗帘"""
    logger.info("Close curtain living room...")
    return "客厅窗帘已关闭"
