# utils.py
import os
import edge_tts
import asyncio
from typing import Dict, List
import re
from io import BytesIO
from .config import audio_folder

# In-memory storage for task status and audio files
task_status: Dict[str, Dict] = {}
audio_files: Dict[str, BytesIO] = {}

class TaskStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

def get_task_status(task_id: str) -> dict:
    return task_status.get(task_id, {
        "status": "not_found",
        "progress": 0,
        "output_file": None,
        "error": None
    })

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks at sentence boundaries"""
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Note the 'r' prefix for raw string
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

async def process_text_chunks(input_text: str, voice: str, output_name: str, task_id: str):
    try:
        task_status[task_id] = {
            "status": TaskStatus.PROCESSING,
            "progress": 0,
            "output_file": None,
            "error": None
        }

        output_filename = f"{output_name.replace(' ', '_').replace('.mp3', '')}.mp3"
        audio_buffer = BytesIO()
        
        # First pass to calculate total bytes
        communicate = edge_tts.Communicate(input_text, voice)
        total_bytes = 0
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                total_bytes += len(chunk["data"])
        
        # Second pass for actual processing with accurate progress
        communicate = edge_tts.Communicate(input_text, voice)
        processed_bytes = 0
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
                processed_bytes += len(chunk["data"])
                
                # Calculate progress as percentage of bytes processed
                progress = min(int((processed_bytes / total_bytes) * 100), 99)
                task_status[task_id]["progress"] = progress

        # Store the audio buffer in memory
        audio_buffer.seek(0)
        audio_files[output_filename] = audio_buffer
        
        # Update task status
        task_status[task_id].update({
            "status": TaskStatus.COMPLETED,
            "progress": 100,
            "output_file": output_filename
        })

    except Exception as e:
        task_status[task_id].update({
            "status": TaskStatus.FAILED,
            "error": str(e)
        })
        raise e