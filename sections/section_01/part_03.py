from autogen import UserProxyAgent, AssistantAgent
import autogen
from duckduckgo_search import DDGS
from typing import Annotated
import json

config_list = autogen.config_list_from_json(
    "../OAI_CONFIG_LIST.json",
)

llm_config = {
    "config_list": config_list,
    "timeout": 600
}


# create user_proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    system_message="Human admin",
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3
)

# create climate_activist agent
climate_activist = AssistantAgent(
    name="climate_activist",
    llm_config=llm_config,
    system_message="You are a climate activist with a vast knowledge on climate change and ways to prevent further climate change."
)


# create rocket_scientist agent
rocket_scientist = AssistantAgent(
    name="rocket_scientist",
    llm_config=llm_config,
    system_message="You are a rocket scientist with avast knowledge on how to design rockets to be efficient. You also take the effect of your rockets on the climate when designing it."
)


groupchat = autogen.GroupChat(
    agents=[rocket_scientist, climate_activist, user_proxy],
    messages=[],
    max_round=100
)


manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# tools


def browse_web(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=1)]
            return results if results else "Not Found"
    except Exception as e:
        print(e)


def web_browser_tool(
    query: Annotated[str,
                     'Query string containing information that you want to search using the internet']
) -> str:
    result = browse_web(query)
    return result


autogen.agentchat.register_function(
    web_browser_tool,
    caller=rocket_scientist,
    executor=user_proxy,
    description="Web browser"
)


autogen.agentchat.register_function(
    web_browser_tool,
    caller=climate_activist,
    executor=user_proxy,
    description="Web browser"
)


# pretty_json = json.dumps(climate_activist.llm_config["tools"], indent=2)
# print(pretty_json)


# initiate conversation
user_proxy.initiate_chat(
    manager,
    message="Discuss on the best way to design rockets to be environmentally friendly and efficient."
)
