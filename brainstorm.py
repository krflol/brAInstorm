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
from openai import OpenAI
import openai



# Load environment variables
dotenv.load_dotenv()

#autogen.api_key = os.getenv("AUTOGEN_API_KEY")  # Make sure to set this environment variable
namespaces = {'xmlns': 'urn:xmind:xmap:xmlns:content:2.0'}
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    def initialize_data(self):
        """
        Initialize or reinitialize the data from the XMind file.
        """
        self.root_topic = self.load_mind_map(self.xmind_file_path)
        self.current_topic = self.root_topic
        self.id_map = {}  # Dictionary to map complex IDs to simple integers
        self.counter = 1  # Counter for simple integer IDs
        self.map_ids(self.root_topic)
        self.list_all_nodes(self.root_topic)


    def do_copy(self, arg):
        """
        Copy the title and content of the current topic to the clipboard.
        """
        if self.current_topic is None:
            print("No topic currently selected.")
            return

        title_elem = self.current_topic.find('{urn:xmind:xmap:xmlns:content:2.0}title')
        if title_elem is None:
            print("No title for this topic.")
            return

        title = title_elem.text
        content = title  # Start with the title

        file_content = self.current_topic.get('file_content')
        if file_content:
            content += "\n\nFile Content:\n" + file_content

        # Copy content to clipboard
        pyperclip.copy(content)
        print("Content copied to clipboard.")
    def do_reload(self, arg):
        """
        Reload the mind map from the file.
        """
        print("Reloading the mind map...")
        self.initialize_data()
        print("Mind map reloaded.")

    def map_ids(self, topic, depth=0):
        """
        Map each topic ID to a simpler integer ID.
        """
        if topic is None:
            print("Error: Attempted to map IDs on a non-existent (None) topic.")
            return  # Exit the method to prevent further errors

        self.id_map[self.counter] = topic
        topic.set('simple_id', str(self.counter))
        self.counter += 1

        # Recursively apply this method to subtopics
        topics_element = topic.find('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics')
        if topics_element is not None:
            for subtopic in topics_element.findall('{urn:xmind:xmap:xmlns:content:2.0}topic'):
                self.map_ids(subtopic, depth + 1)


    def load_mind_map(self, file_path):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                with zip_ref.open('content.xml') as file:
                    xml_content = file.read().decode('utf-8')

            xml_content = xml_content.replace('<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns="urn:xmind:xmap:xmlns:content:2.0">', '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0">', 1)
            content_root = ET.fromstring(xml_content)

            root_topic = content_root.find('{urn:xmind:xmap:xmlns:content:2.0}sheet').find('{urn:xmind:xmap:xmlns:content:2.0}topic')
            self.extract_file_contents(root_topic)
            return root_topic
        except Exception as e:
            print(f"Error loading mind map: {e}")
            return None
        
    def extract_file_contents(self, topic):
        xlink_href = topic.get('{http://www.w3.org/1999/xlink}href')
        if xlink_href and xlink_href.startswith('file://'):
            file_path = xlink_href[7:]  # Remove 'file://' prefix to get the actual file path
            try:
                with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                    file_content = file.read()
                topic.set('file_content', file_content)
                #print(f"File content extracted from {file_path}")
            except UnicodeDecodeError:
                # If utf-8 encoding fails, try a different encoding
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        file_content = file.read()
                    topic.set('file_content', file_content)
                    #print(f"File content extracted from {file_path} using latin-1 encoding")
                except Exception as e:
                    print(f"Error reading file at {file_path} with latin-1 encoding: {e}")
            except Exception as e:
                print(f"Error reading file at {file_path} with utf-8 encoding: {e}")

        for child in topic.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
            self.extract_file_contents(child)


    def do_select(self, simple_id):
        """
        Select a topic by its simple integer ID.
        Usage: select [simple_id]
        """
        try:
            simple_id = int(simple_id)
            topic = self.id_map[simple_id]
            self.current_topic = topic
            print(f"Selected topic with simple ID {simple_id}")
        except (ValueError, KeyError):
            print(f"No topic found with simple ID {simple_id}")

    def do_show(self, arg):
        """
        Show the title of the current topic.
        """
        title_elem = self.current_topic.find('{urn:xmind:xmap:xmlns:content:2.0}title')
        if title_elem is not None:
            print(title_elem.text)
        else:
            print("No title for this topic")

    def do_edit(self, new_title):
        """
        Edit the title of the current topic.
        Usage: edit [new_title]
        """
        title_elem = self.current_topic.find('{urn:xmind:xmap:xmlns:content:2.0}title')
        if title_elem is not None:
            title_elem.text = new_title
            print(f"Title changed to: {new_title}")
        else:
            print("No title to edit for this topic")

    def do_add(self, title):
        """
        Add a new subnode to the current topic with the given title.
        Usage: add [title]
        """
        # Generate a new simple_id by adding 1 to the highest existing simple_id
        new_simple_id = self.get_highest_id(self.root_topic) + 1
        timestamp = str(int(time.time() * 1000))

        # Check if the current topic has a 'children' element, if not, add one
        children = self.current_topic.find('{urn:xmind:xmap:xmlns:content:2.0}children')
        if children is None:
            children = ET.SubElement(self.current_topic, '{urn:xmind:xmap:xmlns:content:2.0}children')

        # Check if 'children' has a 'topics' element of type 'attached', if not, add one
        topics = children.find('{urn:xmind:xmap:xmlns:content:2.0}topics[@type="attached"]')
        if topics is None:
            topics = ET.SubElement(children, '{urn:xmind:xmap:xmlns:content:2.0}topics', attrib={'type': 'attached'})

        # Create a new 'topic' element under 'topics'
        new_topic = ET.SubElement(topics, '{urn:xmind:xmap:xmlns:content:2.0}topic', attrib={
            'id': str(new_simple_id),
            'timestamp': timestamp,
            'simple_id': str(new_simple_id)
        })

        # Create and set the title for the new 'topic'
        new_title = ET.SubElement(new_topic, '{urn:xmind:xmap:xmlns:content:2.0}title')
        new_title.text = title

        # Update the id_map with the new node
        self.id_map[new_simple_id] = new_topic

        print(f"Added new topic with title: {title} and ID: {new_simple_id}")
        self.list_all_nodes(self.root_topic)

    def get_highest_id(self, element, max_id=0):
        """
        Recursively find the highest simple_id in the mind map.
        """
        simple_id = int(element.get('simple_id', 0))
        max_id = max(max_id, simple_id)

        for child in element.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
            max_id = self.get_highest_id(child, max_id)

        return max_id

    def do_remove(self, topic_id):
        """
        Remove a subnode with the specified ID from the current topic.
        Usage: remove [topic_id]
        """
        def remove_topic(element, id):
            for subelement in element.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
                if subelement.get('id') == id:
                    element.remove(subelement)
                    return True
                if remove_topic(subelement, id):
                    return True
            return False

        if remove_topic(self.current_topic, topic_id):
            print(f"Removed topic with ID {topic_id}")
        else:
            print(f"No topic found with ID {topic_id}")

    def do_save(self, arg):
        """
        Save the current mind map back to the XMind file.
        """
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract the existing XMind file contents to the temporary directory
                with zipfile.ZipFile(self.xmind_file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Serialize and write the updated content.xml
                content_xml_path = os.path.join(temp_dir, 'content.xml')
                
                # Create the new root element and sheet element
                xmap_content = ET.Element('xmap-content', {'xmlns': 'urn:xmind:xmap:xmlns:content:2.0'})
                sheet = ET.SubElement(xmap_content, 'sheet')
                
                # Append the existing root topic to the new sheet
                # Deep copy is needed to avoid altering the original root_topic
                copied_root_topic = deepcopy(self.root_topic)
                sheet.append(copied_root_topic)

                # Write the modified XML tree to the content.xml file
                tree = ET.ElementTree(xmap_content)
                tree.write(content_xml_path, encoding='UTF-8', xml_declaration=True)

                # Create a new XMind file, copying other files and replacing content.xml
                with zipfile.ZipFile(self.xmind_file_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                    for folder, subs, files in os.walk(temp_dir):
                        for filename in files:
                            file_path = os.path.join(folder, filename)
                            arcname = os.path.relpath(file_path, temp_dir)
                            new_zip.write(file_path, arcname)

            print(f"Saved changes to {self.xmind_file_path}")
        except Exception as e:
            print(f"Error saving the file: {e}")

    def do_brainstorm(self, additional_context=''):
        context_list = self.extract_context_with_file_content(self.current_topic)
        full_context = ' '.join(context_list)  # Combine context into a single string
        full_prompt = full_context + ' ' + additional_context.strip()

        #print("Final prompt to ChatGPT:", full_prompt)  # Debugging print
        response = self.query_chatgpt(full_prompt)
        print("ChatGPT suggests:", response)    

        if input("Add these sections as subnodes? (y/n): ").lower() == 'y':
            sections = self.split_response_into_sections(response)
            for section in sections:
                self.do_add(section)
    def split_response_into_sections(self, response):
        """
        Split the response into sections using a special cloud character as a delimiter.
        """
        # Split the text using the cloud character as a delimiter
        sections = response.split('🌩️')

        # Trim whitespace for each section
        sections = [section.strip() for section in sections if section.strip()]

        return sections    
    def extract_context_with_file_content(self, topic):
        context = []
        title_elem = topic.find('{urn:xmind:xmap:xmlns:content:2.0}title')
        if title_elem is not None:
            context_str = title_elem.text
            file_content = topic.get('file_content')
            if file_content:
                context_str += f"\n\nFile Content:\n{file_content}\n"  # Adding file content
            context.append(context_str)

        for subtopic in topic.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
            context.extend(self.extract_context_with_file_content(subtopic))

        return context
    
    def query_chatgpt(self, prompt):
        """
        Send a query to ChatGPT using the chat model and return the response.
        """
        try:
            if isinstance(prompt, list):
                prompt = ' '.join(prompt)

            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Correctly extracting the response content
            response_content = response.choices[0].message.content.strip()
            return response_content
        except Exception as e:
            print("Error querying ChatGPT:", e)
            return ""                


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
            system_message='we are using a mind map to organize our ideas and manage the project.',
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
        context_list = self.extract_context_with_file_content(self.current_topic)
        full_context = ' '.join(context_list)  # Combine context into a single string
        full_prompt = full_context + ' ' + prompt.strip()
        self.user_proxy.initiate_chat(self.manager, message=full_prompt, clear_history=True)

        autogen_responses = []
        try:
            while "TERMINATE" not in autogen_responses[-1]:
                #sleep for 30 seconds
                time.sleep(120)
                self.manager.step()
                responses = [message.content for message in self.groupchat.latest_messages]
                autogen_responses.extend(responses)
        except IndexError:
            print("No responses from Autogen.")
            pass
        for suggestion in autogen_responses:
            print("Autogen suggests:", suggestion)
            if input("Add this section as a subnode? (y/n): ").lower() == 'y':
                self.do_add(suggestion.strip())


    def list_all_nodes(self, topic, depth=0):
        if topic is None:
            print("Error: Topic is None in list_all_nodes")
            return  # Exit if topic is None

        title_elem = topic.find('{urn:xmind:xmap:xmlns:content:2.0}title')
        if title_elem is not None:
            simple_id = topic.get('simple_id')
            title = ' '.join(title_elem.text.split()[:10])
            print('  ' * depth + f"{title} (ID: {simple_id})")

        for subtopic in topic.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
            self.list_all_nodes(subtopic, depth + 1)

    def do_list_nodes(self, arg):
        """
        List all nodes with their simple integer IDs.
        
        """
        

        self.list_all_nodes(self.root_topic)

    def do_exit(self, arg):
        """
        Exit the Mind Map Editor CLI.
        """
        print("Exiting Mind Map Editor CLI...")
        return True

# Check if the filename is provided
if len(sys.argv) < 2:
    print("Usage: python brainstorm.py [filename.xmind]")
else:
    filename = sys.argv[1]
    cli = MindMapEditorCLI(filename)
    cli.cmdloop()
