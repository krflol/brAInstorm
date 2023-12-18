# filename: test_brainstorm.py

import sys
import subprocess
import json

# Verify if OAI_CONFIG_LIST.json is present and properly formatted
try:
    with open('OAI_CONFIG_LIST.json') as file:
        config_json = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    sys.exit(f"Error with 'OAI_CONFIG_LIST.json': {e}")

# Assume that the environment variables are set in the environment or through a .env file
# Add code to execute the brainstorm.py script
try:
    subprocess.run(['python', 'brainstorm.py', '<YOUR_XMIND_FILE_HERE.xmind>'], check=True)
except subprocess.CalledProcessError as e:
    sys.exit(f"The script failed with return code: {e.returncode}")