
import cmd
import xml.etree.ElementTree as ET
import zipfile
import sys
import dotenv
import os
import tempfile
import shutil
import time
from copy import deepcopy
import re
import pyperclip
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager
import autogen

# Load environment variables
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
autogen.api_key = os.getenv("AUTOGEN_API_KEY")  # Make sure to set this environment variable
namespaces = {'xmlns': 'urn:xmind:xmap:xmlns:content:2.0'}
# Register the namespace
ET.register_namespace('', namespaces['xmlns'])

class MindMapEditorCLI(cmd.Cmd):
    intro = 'Welcome to brAInstorm. Type help or ? to list commands.\n'
    prompt = '(brAInstorm) '

    def __init__(self, xmind_file_path):
        super().__init__()
        self.xmind_file_path = xmind_file_path
        self.root_topic = self.load_mind_map(xmind_file_path)
        self.current_topic = self.root_topic
        self.id_map = {}
        self.counter = 1
        self.map_ids(self.root_topic)
        self.list_all_nodes(self.root_topic)
        self.initialize_autogen()

    # ... (existing methods)

    def initialize_autogen(self):
        config_list_gpt4 = config_list_from_json(
            "OAI_CONFIG_LIST.json",
            filter_dict={
                "model": ["gpt-4-1106-preview", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
            },
        )
        llm_config = {"config_list": config_list_gpt4, "seed": 42}
        self.user_proxy = UserProxyAgent(
            name="User_proxy",
            system_message='',
            code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
            default_auto_reply="proceed with implementation. I will execute any code locally and send you the results.",
            human_input_mode="TERMINATE"
        )
        self.coder = AssistantAgent(
            name="Coder",
            llm_config=llm_config,
        )
        self.pm = AssistantAgent(
            name="Product_manager",
            system_message="An expert in project management and research",
            llm_config=llm_config,
        )
        self.groupchat = GroupChat(agents=[self.user_proxy, self.coder, self.pm], messages=[], max_round=12)
        self.manager = GroupChatManager(groupchat=self.groupchat, llm_config=llm_config)

    def do_autogen(self, prompt):
        """
        Start a brainstorming session using Autogen.
        Usage: autogen [prompt]
        """
        self.user_proxy.initiate_chat(self.manager, message=prompt, clear_history=True)

        autogen_responses = []
        while not self.groupchat.terminated:
            self.manager.step()
            responses = [message.content for message in self.groupchat.latest_messages]
            autogen_responses.extend(responses)

        for suggestion in autogen_responses:
            print("Autogen suggests:", suggestion)
            if input("Add this section as a subnode? (y/n): ").lower() == 'y':
                self.do_add(suggestion.strip())

    # ... (rest of the existing methods)

# Check if the filename is provided
if len(sys.argv) < 2:
    print("Usage: python brainstorm.py [filename.xmind]")
else:
    filename = sys.argv[1]
    cli = MindMapEditorCLI(filename)
    cli.cmdloop()
