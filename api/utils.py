import os
import edge_tts

async def generate_audio_and_subtitles_from_text(input_text: str, voice: str, output_name: str, audio_folder: str, subtitles_folder: str) -> tuple:
    output_audio_file = output_name.replace(" ", "_") + ".mp3"
    output_subtitle_file = output_name.replace(" ", "_") + ".vtt"
    try:
        communicate = edge_tts.Communicate(input_text, voice)
        submaker = edge_tts.SubMaker()
        async for chunk in communicate.stream():
            if chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        with open(os.path.join(audio_folder, output_audio_file), "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

        with open(os.path.join(subtitles_folder, output_subtitle_file), "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())
        return output_audio_file, output_subtitle_file
    except Exception as e:
        raise e
