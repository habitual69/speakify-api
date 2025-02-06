# utils.py
import os
import edge_tts
import asyncio
from typing import Dict, List
import re
from .config import audio_folder


# In-memory storage for task status
task_status: Dict[str, Dict] = {}

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

        # Create output filename
        output_filename = f"{output_name.replace(' ', '_')}.mp3"
        output_filepath = os.path.join(audio_folder, output_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

        # Process entire text at once
        communicate = edge_tts.Communicate(input_text, voice)
        total_bytes = 0
        processed_bytes = 0
        
        # First pass to calculate total bytes
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                total_bytes += len(chunk["data"])
        
        # Reset communicator for actual processing
        communicate = edge_tts.Communicate(input_text, voice)
        
        with open(output_filepath, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                    processed_bytes += len(chunk["data"])
                    
                    # Update progress based on bytes processed
                    if total_bytes > 0:
                        progress = min(int((processed_bytes / total_bytes) * 100), 99)
                        task_status[task_id]["progress"] = progress

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