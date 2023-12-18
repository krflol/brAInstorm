from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager
import autogen
import dotenv
import json
#from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent


config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-1106-preview", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

llm_config = {"config_list": config_list_gpt4, "seed": 42}
user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   system_message='''
''',
   code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
   default_auto_reply="proceed with implementation. I will execute any code locally and send you the results.",
   human_input_mode="TERMINATE"
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="An expert in and project management and research",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message='''''', clear_history=False)
# type exit to terminate the chat