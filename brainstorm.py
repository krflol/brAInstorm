import cmd
import xml.etree.ElementTree as ET
import zipfile
import sys
import openai

class MindMapEditorCLI(cmd.Cmd):
    intro = 'Welcome to the Mind Map Editor CLI. Type help or ? to list commands.\n'
    prompt = '(mindmap) '

    def __init__(self, xmind_file_path):
        super().__init__()
        self.xmind_file_path = xmind_file_path
        self.root_topic = self.load_mind_map(xmind_file_path)
        self.current_topic = self.root_topic

    def load_mind_map(self, file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extract('content.xml', '/mnt/data')
            content_xml_path = '/mnt/data/content.xml'
            content_root = ET.parse(content_xml_path).getroot()
            return content_root.find('{urn:xmind:xmap:xmlns:content:2.0}sheet').find('{urn:xmind:xmap:xmlns:content:2.0}topic')

    def do_select(self, topic_id):
        """
        Select a topic by its ID.
        Usage: select [topic_id]
        """
        def find_topic(element, id):
            if element.get('id') == id:
                return element
            for subelement in element.findall('{urn:xmind:xmap:xmlns:content:2.0}children/{urn:xmind:xmap:xmlns:content:2.0}topics/{urn:xmind:xmap:xmlns:content:2.0}topic'):
                result = find_topic(subelement, id)
                if result:
                    return result
            return None

        topic = find_topic(self.root_topic, topic_id)
        if topic:
            self.current_topic = topic
            print(f"Selected topic with ID {topic_id}")
        else:
            print(f"No topic found with ID {topic_id}")

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
        new_topic = ET.SubElement(self.current_topic, '{urn:xmind:xmap:xmlns:content:2.0}topic')
        new_title = ET.SubElement(new_topic, '{urn:xmind:xmap:xmlns:content:2.0}title')
        new_title.text = title
        print(f"Added new topic with title: {title}")

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
        with zipfile.ZipFile(self.xmind_file_path, 'w') as zip_ref:
            zip_ref.writestr('content.xml', ET.tostring(self.root_topic))
            print(f"Saved changes to {self.xmind_file_path}")

    def do_brainstorm(self, additional_context=''):
        """
        Use ChatGPT to brainstorm ideas based on the current topic.
        Usage: brainstorm [additional_context]
        """
        context =
