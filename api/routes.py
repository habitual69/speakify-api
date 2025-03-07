# routes.py
from fastapi import APIRouter, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from .config import voices
from .utils import process_text_chunks, get_task_status, TaskStatus, audio_files
import uuid

router = APIRouter()

@router.get("/voices")
async def get_voices():
    return voices

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
    if output_file in audio_files:
        audio_buffer = audio_files[output_file]
        audio_buffer.seek(0)
        
        # Remove the file from memory after sending
        def cleanup():
            yield audio_buffer.getvalue()
            audio_files.pop(output_file, None)
        
        return StreamingResponse(
            cleanup(),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={output_file}"}
        )
    else:
        raise HTTPException(status_code=404, detail="Audio file not found.")

