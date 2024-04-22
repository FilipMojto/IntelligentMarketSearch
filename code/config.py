import json
import os, sys

def get_config_path():
    if getattr(sys, 'frozen', False):
        # If the script is run as an executable (e.g., PyInstaller bundle)
        return os.path.join(os.path.dirname(sys.executable), "..\\config.json")
    else:
        # If the script is run as a Python script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_directory, ".config.json")

# ------ Project Config Globals ------ #

CONFIG_FILE_PATH = get_config_path()

# Load the JSON metadata file
with open(CONFIG_FILE_PATH, 'r') as file:
    metadata = json.load(file)

# Extract column names
PF_FIELDNAMES = list(metadata['resources']['data']['products']['columns'].keys())
