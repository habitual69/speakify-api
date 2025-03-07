# config.py
import os
import json

# Get the current directory (where config.py is located)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define audio folder path relative to the base directory
audio_folder = os.path.join(BASE_DIR, "audio")
tmp_folder = os.path.join(BASE_DIR, "tmp")

# How long to keep files (in hours) before deletion
file_retention_hours = 24  # Files will be deleted after 24 hours

# Create audio and tmp directories if they don't exist
try:
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(tmp_folder, exist_ok=True)
except Exception as e:
    print(f"Error creating folders: {e}")
    raise

# Load available voices from voices.json
try:
    voice_file = os.path.join(BASE_DIR, "voices.json")
    with open(voice_file, "r") as f:
        voices = json.load(f)
except FileNotFoundError:
    voices = []
