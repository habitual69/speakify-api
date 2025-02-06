from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
import uvicorn
from pyngrok import ngrok

app = FastAPI(title="Speakify", version="1.0.0")

# Add CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Start ngrok tunnel
public_url = ngrok.connect(8000).public_url
print(f"🚀 Speakify API Public URL: {public_url}")

@app.get("/")
async def root():
    return {
        "Author": "Habitual69",
        "Github": "https://github.com/habitual69",
        "Project Name": "Speakify",
        "Description": "A simple API to generate audio and subtitles from text.",
        "Version": "1.0.0",
        "Docs": "/docs",
        "API": "/api/v1",
        "Public URL": public_url,  # Return ngrok URL
        "Endpoints": {
            "/voices": "Get a list of available voices.",
            "/convert": "Generate audio and subtitles from text.",
            "/audio/{output_file}": "Get the audio file.",
            "/subtitles/{output_file}": "Get the subtitles file."
        },
        "Example": {
            "input_text": "Hello, how are you?",
            "voice": "en-US-JennyNeural",
            "output_name": "output"
        },
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
