

# Mind Map Editor CLI (brAInstorm)

The Mind Map Editor CLI, named "brAInstorm," is a command-line application for interacting with XMind mind maps. It allows users to edit, view, and manage mind map topics, integrate with OpenAI's GPT models for brainstorming, and more.
[![Video Title](https://img.youtube.com/vi/wp6bOKYFHZo/0.jpg)](https://www.youtube.com/watch?v=wp6bOKYFHZo)
[![Video Title](https://img.youtube.com/vi/V7i2284UoEk/0.jpg)](https://www.youtube.com/watch?v=V7i2284UoEk)

## Features
- Load and edit XMind mind maps.
- Copy content to clipboard.
- Reload mind maps from file.
- Add, edit, and remove topics.
- List all topics and nodes.
- Integrate with OpenAI's GPT models for brainstorming sessions.
- Autogen support for collaborative brainstorming.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repository/brainstorm.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd brainstorm
   ```

3. **Install required dependencies:**
   - Ensure that Python 3.6 or later is installed.
   - Install the required Python packages:
     ```bash
     pip install cmd xml.etree.ElementTree zipfile sys dotenv os tempfile shutil time copy re pyperclip autogen openai
     ```

## Usage

1. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_api_key_here
     ```

2. **Run the CLI:**
   ```bash
   python brainstorm.py [filename.xmind]
   ```
   Replace `[filename.xmind]` with the path to your XMind file.

3. **Use CLI commands:**
   - Type `help` or `?` to list available commands.
   - Use commands like `add`, `edit`, `remove`, `list_nodes`, and others to interact with the mind map.

## Note
- This application requires a valid OpenAI API key for certain features like brainstorming with GPT models.
- The XMind file must follow a specific structure to be compatible with this CLI.

