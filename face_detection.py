import base64
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv

# Load credentials
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
buffer = []

@app.get("/")
async def root():
    return {"message": "VRM Voice Proxy is running"}

@app.post("/tts")
async def text_to_speech(request: Request):
    try:
        data = await request.json()
        text = data.get("text")
        
        if not text or not ELEVENLABS_API_KEY:
            return {"error": "Missing text or API key"}

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        # Multilingual v2 is perfect for Tamil, Telugu, and English
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code != 200:
                print(f"ElevenLabs Error: {response.text}")
                return {"error": "Failed to generate speech"}
            
            # Return as base64 to frontend
            audio_b64 = base64.b64encode(response.content).decode('utf-8')
            return {"audio": audio_b64}

    except Exception as e:
        print("TTS Error:", e)
        return {"error": str(e)}

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "voice_configured": bool(ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID)
    }

if __name__ == "__main__":
    uvicorn.run("face_detection:app", host="0.0.0.0", port=8001, reload=False)