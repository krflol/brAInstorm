# Let's read the content of the uploaded content.xml file to understand its structure.
content_xml_path = r'C:\dev\brAInstorm\content.xml'

# Function to read the content of a file
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Read and return the content of content.xml
content_xml_data = read_file_content(content_xml_path)
content_xml_data[:1000]  # Displaying the first 1000 characters for a brief look
