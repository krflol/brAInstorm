
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


    # ... (rest of the existing methods)

# Check if the filename is provided
if len(sys.argv) < 2:
    print("Usage: python brainstorm.py [filename.xmind]")
else:
    filename = sys.argv[1]
    cli = MindMapEditorCLI(filename)
    cli.cmdloop()
