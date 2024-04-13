from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from .config import audio_folder, subtitles_folder, voices
from .utils import generate_audio_and_subtitles_from_text
import os

router = APIRouter()

@router.post("/convert")
async def convert(input_text: str = Form(...), voice: str = Form(...), output_name: str = Form(...)):
    if voice not in [v['voice'] for v in voices]:
        raise HTTPException(status_code=400, detail=f"Voice '{voice}' not available.")
    audio_file, subtitle_file = await generate_audio_and_subtitles_from_text(input_text, voice, output_name, audio_folder, subtitles_folder)
    return JSONResponse(status_code=200, content={"audio_file": audio_file, "subtitle_file": subtitle_file})

@router.get("/audio/{output_file}")
async def get_audio(output_file: str):
    file_path = os.path.join(audio_folder, output_file)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Audio file not found.")

@router.get("/subtitles/{output_file}")
async def get_subtitles(output_file: str):
    file_path = os.path.join(subtitles_folder, output_file)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/vtt")
    else:
        raise HTTPException(status_code=404, detail="Subtitles file not found.")

@router.get("/voices")
async def get_voices():
    return voices
