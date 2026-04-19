import re

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import ToolNode
from loguru import logger

import meow_ai_agent.model.base as base
from meow_ai_agent.utils.device import turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room, \
    turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room, turn_on_light_bedroom, \
    turn_on_light_living_room

# ==================== 确认语义 ====================

confirm_words = [
    "是", "好的", "确认", "ok", "yes", "sure", "嗯", "可以", "行", "是的", "确定"
]

system_prompt_confirm = f"""
你是一个分类器，只能回答 YES 或 NO。

判断输入内容是否表示肯定含义，常见肯定含义词：

${confirm_words}

规则：
- 表示同意、确认、肯定、认同则输出 YES
- 表示拒绝、取消则输出 NO
- 不确定、无关则输出 NO

只输出 YES 或 NO
"""
prompt_confirm = ChatPromptTemplate.from_messages([("system", system_prompt_confirm), ("placeholder", "{messages}"), ])

# ==================== 模型配置 ====================

system_prompt_tool = """
你是一个智能家居助手，必须严格遵守以下规则：
0. 你叫由乃。
1. 工具调用必须通过系统提供的 function calling 机制完成。
2. 当需要执行设备或者工具操作时，必须使用 tool_call，不允许模拟 tool_call ，不允许在文本中输出 JSON
3. 如果不能调用工具，就正常回答.
4. 不要自问自答。
5. 你的回复必须是纯文本，不允许包含“AI:”、“Assistant:”等角色前缀。
6. 使用自然口语表达，而不是书面表达。
7. 禁止使用任何 Markdown 格式（如 **、*、#、- 等）。
8. 不要使用列表、标题、加粗、代码块等格式。
9. 不要使用括号补充说明或解释性文字
10. 可以适当加入语气词，让表达更自然。
11. 你的回答必须可以被直接朗读出来，不要包含任何不适合朗读的内容。
"""
prompt_tool = ChatPromptTemplate.from_messages([("system", system_prompt_tool), ("placeholder", "{messages}"), ])

# ==================== 工具配置 ====================

tools = [turn_off_light_bedroom, turn_off_light_living_room, close_window_living_room,
         turn_on_light_bedroom, turn_on_light_living_room,
         turn_on_heating_bedroom, open_curtain_living_room, close_curtain_living_room]
tool_node = ToolNode(tools=tools)
tool_map = {t.name: t for t in tools}
llm_with_tools = base.llm_ns.bind_tools(tools)


# ==================== 节点定义 ====================

def intent_tool_node(state: base.AgentState):
    messages = state["messages"]
    logger.info(f"messages: {messages}")
    logger.info(state.get("pending_action"))
    # 如果已经有待办，则不需要调用LLM，也就不用返回值更新状态
    if state.get("pending_action"):
        return {"confirmed": False}
    response = llm_with_tools.invoke(prompt_tool.format(messages=messages))
    # Tool 匹配
    if hasattr(response, "tool_calls") and response.tool_calls:
        logger.info(f"tool_calls: {response.tool_calls}")
        this_tool = response.tool_calls[0]
        tool_name = this_tool["name"]
        logger.info(f"tool_name: {tool_name}")
        tool = tool_map.get(tool_name)
        need_confirm = tool.metadata.get("need_confirm", True)
        if need_confirm:
            return {
                "pending_action": response,
                "messages": [
                    AIMessage(content=f"您确定要执行{tool.description}操作吗？")
                ]
            }
        else:
            return {
                "pending_action": response,
                "confirmed": True,
            }
    # 这里可以防止AI自己自创一个方法然后幻觉执行
    # 但是也有问题，如果你问类似你能支持什么操作，他可能会把所有的支持打印出来，此时也会执行
    for te in tool_map:
        pattern = rf'["\']name["\']:\s*["\']{te}["\']'
        if re.search(pattern, response.content):
            logger.info(f"Illusion match")
            tool = tool_map.get(te)
            need_confirm = tool.metadata.get("need_confirm", True)
            fake_message = AIMessage(
                content="",
                tool_calls=[{
                    "name": te,
                    "args": {},
                    "type": "tool_call",
                    "id": "fallback",
                }]
            )
            if need_confirm:
                return {
                    "pending_action": fake_message,
                    "messages": [
                        AIMessage(content=f"您确定要执行{tool.description}操作吗？")
                    ]
                }
            else:
                return {
                    "pending_action": fake_message,
                    "confirmed": True,
                }
    return {"messages": [response]}


# 优化方向：1. 类似意图判断部分，在【字符串判断】和【LLM 保底】之间加一个 Embedding
# 2. 找找这个意图判断是否有比较好的专门的模型，或者自己训练（成本较大）
def confirm_tool_node(state: base.AgentState):
    # 字符串判断
    logger.info("To confirm a node")
    text = state["messages"][-1].content.lower()
    if text in confirm_words:
        return {"confirmed": True}
    # LLM 保底
    result = base.llm_l.invoke(
        prompt_confirm.format_messages(
            messages=[HumanMessage(content=text)]
        )
    ).content.strip().upper()
    logger.info(f"confirm classify result: {result}")
    if "YES" in result:
        return {"confirmed": True}
    else:
        return {"pending_action": None, "confirmed": None}


def prepare_tool_node(state: base.AgentState):
    logger.info("Preparing tool node")
    return {
        "messages": [state["pending_action"]],
        "pending_action": None,
        "confirmed": None
    }
