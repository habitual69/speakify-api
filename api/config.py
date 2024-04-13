import os
import json

output = "/tmp"
audio_folder = os.path.join(output, "audio")
subtitles_folder = os.path.join(output, "subtitles")

# Create folders if they don't exist
for folder in [audio_folder, subtitles_folder]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# Load available voices from voices.json
with open("voices.json", "r") as f:
    voices = json.load(f)
