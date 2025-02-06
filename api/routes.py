# routes.py
from fastapi import APIRouter, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from .config import audio_folder, voices
from .utils import process_text_chunks, get_task_status, TaskStatus
import os
import uuid

router = APIRouter()

@router.post("/convert")
async def convert(background_tasks: BackgroundTasks, 
                 input_text: str = Form(...), 
                 voice: str = Form(...), 
                 output_name: str = Form(...)):
    if voice not in [v['Voice'] for v in voices]:
        raise HTTPException(status_code=400, detail=f"Voice '{voice}' not available.")
    
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        process_text_chunks,
        input_text=input_text,
        voice=voice,
        output_name=output_name,
        task_id=task_id
    )
    
    return JSONResponse(
        status_code=202, 
        content={
            "task_id": task_id,
            "message": "Processing started",
            "status_endpoint": f"/status/{task_id}"
        }
    )

@router.get("/status/{task_id}")
async def check_status(task_id: str):
    status = get_task_status(task_id)
    return JSONResponse(content=status)

@router.get("/audio/{output_file}")
async def get_audio(output_file: str):
    file_path = os.path.join(audio_folder, output_file)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Audio file not found.")

@router.get("/voices")
async def get_voices():
    return voices