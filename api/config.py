# config.py
import os
import json

# Get the current directory (where config.py is located)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define audio folder path relative to the base directory
audio_folder = os.path.join(BASE_DIR, "audio")

# Create audio directory if it doesn't exist
try:
    os.makedirs(audio_folder, exist_ok=True)
except Exception as e:
    print(f"Error creating audio folder: {e}")
    raise

# Load available voices from voices.json
try:
    voice_file = os.path.join(BASE_DIR, "voices.json")
    with open(voice_file, "r") as f:
        voices = json.load(f)
except FileNotFoundError:
    voices = []
