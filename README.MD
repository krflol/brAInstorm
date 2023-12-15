


# brAInstorm Mind Map Editor CLI
[![Video Title](https://img.youtube.com/vi/V7i2284UoEk/0.jpg)](https://www.youtube.com/watch?v=V7i2284UoEk)

`brAInstorm` is a command-line interface tool designed for creating and manipulating mind maps in XMind format. It integrates with OpenAI's GPT-4 to enhance brainstorming sessions, allowing for AI-powered suggestions and ideas.

## Features

- Load and save XMind formatted mind maps.
- Navigate and manipulate mind map nodes using simple integer IDs.
- Use ChatGPT to brainstorm ideas based on the current topic.
- Extract and utilize file contents linked in mind maps.
- Copy the content of the currently selected node to the clipboard.

## Installation

To use `brAInstorm`, you need Python installed on your system. Clone or download this repository to your local machine.

You also need to install some dependencies:

```bash
pip install pyperclip openai
```

Make sure to have an OpenAI API key set as an environment variable or in a `.env` file in the project directory with the key `OPENAI_API_KEY`.

## Usage

To start `brAInstorm`, navigate to the directory containing `brainstorm.py` and run:

```bash
python brainstorm.py [filename.xmind]
```

Replace `[filename.xmind]` with the path to your XMind file.

## Commands

- `select [simple_id]`: Select a node by its simple integer ID.
- `show`: Display the title of the current node.
- `edit [new_title]`: Edit the title of the current node.
- `add [title]`: Add a new subnode with the specified title.
- `remove [topic_id]`: Remove a node by its ID.
- `save`: Save changes back to the XMind file.
- `reload`: Reload the mind map from the file.
- `copy`: Copy the title and content of the current node to the clipboard.
- `brainstorm [additional_context]`: Use ChatGPT to brainstorm ideas.
- `list_nodes`: List all nodes with their IDs.
- `exit`: Exit the CLI.
## License

[Your chosen license]

## Contributing

Contributions to `brAInstorm` are welcome. Please ensure to follow the code of conduct and contribution guidelines.

## Contact

For support or queries, contact [Your Contact Information].

```

This README provides a basic overview, installation instructions, usage guidelines, and a list of commands. You can expand it further with more detailed explanations, screenshots, or any additional information you think would be helpful for users.
