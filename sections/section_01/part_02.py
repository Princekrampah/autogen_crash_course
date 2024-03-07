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

# create assistant agent
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="For currency conversion tasks, only use the functions you have been provided with. Reply with TERMINATE once your task is done."
)

# create user_proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER"
)


def exchange_rate(query: str) -> str:
    try:
        with DDGS() as ddgs:
            result = [r for r in ddgs.text(query, max_results=1)]
            return result if result else "No result found"
    except Exception as e:
        raise ValueError(
            f"Error: {e}"
        )
        

def currency_calculator(query: Annotated[str, "Query string which currency conversion is required."]) -> str:
    quote_amount = exchange_rate(query)
    return quote_amount


autogen.agentchat.register_function(
    currency_calculator,
    caller=assistant,
    executor=user_proxy,
    description="Used for currency conversion"
)


# print(assistant.llm_config["tools"])
    
    
# pretty_json = json.dumps(assistant.llm_config["tools"], indent=2)
# print(pretty_json)


user_proxy.initiate_chat(
    assistant,
    message="How much is 123.45 USD in EUR?"
)