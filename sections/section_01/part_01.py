from autogen import UserProxyAgent, AssistantAgent
import autogen

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
    llm_config=llm_config
)

# create user_proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER"
)

# initializer messages
user_proxy.initiate_chat(
    assistant,
    message="Tell me about the second world war"
)

