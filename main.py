from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
import uvicorn
from pyngrok import ngrok, conf
import os

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

# Set ngrok auth token from environment variable
ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN")
if ngrok_auth_token:
    conf.get_default().auth_token = ngrok_auth_token

# Ensure ngrok tunnel is only created once
try:
    # Check if ngrok tunnel is already running
    tunnels = ngrok.get_tunnels()
    if tunnels:
        public_url = tunnels[0].public_url
        print(f"🔗 Reusing existing ngrok URL: {public_url}")
    else:
        # Create a new tunnel if none exists
        public_url = ngrok.connect(8000).public_url
        print(f"🚀 New ngrok URL: {public_url}")
except Exception as e:
    public_url = "Error: Could not start ngrok"
    print(f"⚠️ ngrok error: {e}")

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
