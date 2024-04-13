Sure! Here's the updated README.md with descriptions of the uses of all the endpoints:

---

# Speakify API

Speakify is a simple API that generates audio and subtitles from text using text-to-speech (TTS) technology. It provides an easy-to-use interface to convert text into audio files (in MP3 format) and corresponding subtitle files (in VTT format) with various available voices.

## Usage

### Endpoints

- `POST /api/v1/convert`: Generates audio and subtitles from input text.
  - **Parameters**: 
    - `input_text`: The text to convert into audio and subtitles.
    - `voice`: The voice to use for TTS. Available voices can be obtained from the `/api/v1/voices` endpoint.
    - `output_name`: The desired name for the output audio and subtitle files.
  - **Response**: JSON object containing the URLs of the generated audio and subtitle files.
  - **Use**: Use this endpoint to convert text into audio and subtitles. This is useful for generating audio files with corresponding subtitles for various purposes such as video production, accessibility features, and language learning applications.

- `GET /api/v1/audio/{output_file}`: Retrieves the generated audio file.
  - **Parameters**: 
    - `output_file`: The name of the audio file generated from the conversion.
  - **Response**: The audio file in MP3 format.
  - **Use**: Use this endpoint to fetch the generated audio file. This is useful for downloading the audio file for playback or integration into other applications.

- `GET /api/v1/subtitles/{output_file}`: Retrieves the generated subtitle file.
  - **Parameters**: 
    - `output_file`: The name of the subtitle file generated from the conversion.
  - **Response**: The subtitle file in VTT format.
  - **Use**: Use this endpoint to fetch the generated subtitle file. This is useful for downloading the subtitle file for use in video editing software or for displaying subtitles alongside the audio.

- `GET /api/v1/voices`: Retrieves the list of available voices for TTS.
  - **Response**: List of available voices with their names and language codes.
  - **Use**: Use this endpoint to get a list of available voices for text-to-speech conversion. This is useful for providing voice selection options to users or programmatically selecting voices based on language or preference.

### Example

```bash
# Request
curl -X POST https://your-domain.com/api/v1/convert \
  -d 'input_text=Hello, how are you?' \
  -d 'voice=en-US-JennyNeural' \
  -d 'output_name=output'

# Response
{
  "audio_file": "output.mp3",
  "subtitle_file": "output.vtt"
}
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/habitual69/speakify-api.git
```

2. Install dependencies:

```bash
cd speakify-api
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.