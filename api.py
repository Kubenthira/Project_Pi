import base64
import json
import logging
import os
import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq
from scoring import get_behavioral_analysis

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VRM-Proxy")

# Load credentials
load_dotenv(override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not found in .env!")
if not SARVAM_API_KEY:
    logger.warning("SARVAM_API_KEY not found in .env!")

session_history = {}

# Step 7: Safety Escalation Resources
SAFETY_RESOURCES = {
    "en-IN": "I've detected a high level of distress. Please know that you are not alone. Please reach out to a professional or a helpline: iCall (9152987821) or Vandrevala Foundation (18602662345).",
    "ta-IN": "அதிக மன உளைச்சலை நான் உணர்கிறேன். நீங்கள் தனியாக இல்லை. தயவுசெய்து உதவிக்கு அழைக்கவும்: iCall (9152987821) அல்லது Vandrevala Foundation (18602662345).",
    "hi-IN": "मैंने बहुत अधिक संकट महसूस किया है। कृपया जानें कि आप अकेले नहीं हैं। कृपया किसी पेशेवर या हेल्पलाइन से संपर्क करें: iCall (9152987821) या Vandrevala Foundation (18602662345)।"
}

app = FastAPI()

# Lazy-loading clients to prevent startup crashes on Vercel
_groq_client = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing. Please set it in Vercel environment variables.")
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_event(msg):
    # Log to console only (Vercel logs)
    logger.info(msg)

@app.get("/")
async def root():
    return {
        "message": "AI Avatar Proxy is running",
        "port": 8016,
        "brain": "Groq Llama-3 (8B)",
        "voice": "Sarvam Shruti"
    }

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("text", "")
        emotion_data = data.get("emotion_data", {}) # New: Receive emotion signals
        
        # Log signals
        if emotion_data:
            log_event(f"Signals Received - Emotion: {emotion_data.get('emotion')}, Confidence: {emotion_data.get('score')}")
        
        # Get session ID (default to 'global' if not provided)
        session_id = data.get("session_id", "default_user")
        if session_id not in session_history:
            session_history[session_id] = []
            
        # Step 2: Behavioral Analysis with History
        analysis = get_behavioral_analysis(message, emotion_data, session_history[session_id])
        
        # Update history (keep last 5)
        session_history[session_id].append(analysis)
        if len(session_history[session_id]) > 5:
            session_history[session_id].pop(0)

        log_event(f"Analysis - State: {analysis['state']}, Risk: {analysis['risk_score']}")

        # Phase 2: Step 7 - Safety Circuit Breaker
        if analysis['risk_score'] >= 0.8:
            log_event(f"SAFETY TRIGGERED: High Risk ({analysis['risk_score']}) detected for {session_id}")
            lang = data.get("lang", "en-IN")
            safety_msg = SAFETY_RESOURCES.get(lang, SAFETY_RESOURCES["en-IN"])
            return {
                "response": safety_msg,
                "lang": lang,
                "analysis": analysis,
                "safety_triggered": True
            }

        if not message:
            return {"response": "I'm listening! What's on your mind?", "lang": "en-IN", "analysis": analysis}

        system_prompt = (
            "You are a compassionate and supportive mental health companion (MindfulAI). "
            f"ANALYSIS: The user's current state is classified as '{analysis['state']}' with a risk score of {analysis['risk_score']:.2f}. "
            f"STRATEGY: You MUST prioritize using the following technique: '{analysis['selected_technique']}'. "
            "Follow the 'Validation-First Rule': Always acknowledge the user's emotion before suggesting the technique. "
            "Keep responses short, safe, and validating. DO NOT diagnose medical conditions. "
            "CRITICAL: Your response MUST be a JSON object with two keys: 'response' and 'lang'. "
            "Example: {\"response\": \"I hear that you're feeling overwhelmed. Let's try a quick breathing exercise...\", \"lang\": \"en-IN\"}. "
        )
        
        try:
            client = get_groq_client()
            # Use llama-3.1-8b-instant as the replacement model
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                response_format={"type": "json_object"}
            )
            
            raw_response = completion.choices[0].message.content
            log_event(f"Groq Response: {raw_response}")
            
            res_data = json.loads(raw_response)
            if "response" not in res_data: res_data["response"] = "Honey, I'm here for you!"
            if "lang" not in res_data: res_data["lang"] = "en-IN"
            res_data["analysis"] = analysis
            return res_data
            
        except Exception as groq_err:
            log_event(f"Groq Error: {str(groq_err)}")
            return {"response": "I'm a bit shy right now. Can we talk again in a moment?", "lang": "en-IN"}

    except Exception as e:
        log_event(f"Chat Exception: {str(e)}")
        return {"error": "Server error in processing chat."}

@app.post("/tts_sarvam")
async def tts_sarvam(request: Request):
    try:
        data = await request.json()
        text = data.get("text")
        lang = data.get("lang", "en-IN")

        if not text:
            return {"error": "No text provided for TTS"}

        sarvam_lang = lang if lang in ["ta-IN", "te-IN", "hi-IN", "en-IN"] else "en-IN"
        url = "https://api.sarvam.ai/text-to-speech"
        headers = { 
            "api-subscription-key": SARVAM_API_KEY, 
            "Content-Type": "application/json" 
        }
        
        payload = {
            "inputs": [text],
            "target_language_code": sarvam_lang,
            "speaker": "shruti",
            "model": "bulbul:v3"
        }
        log_event(f"Sarvam Request: {text[:30]}... ({sarvam_lang})")

        async with httpx.AsyncClient() as client_http:
            response = await client_http.post(url, json=payload, headers=headers, timeout=30.0)
            
            if response.status_code != 200:
                log_event(f"Sarvam Error: {response.status_code} - {response.text}")
                # Fallback to 'meera' speaker if 'shruti' fails
                if "speaker" in response.text.lower() or response.status_code == 400:
                   log_event("Falling back to Meera speaker...")
                   payload["speaker"] = "meera"
                   response = await client_http.post(url, json=payload, headers=headers, timeout=30.0)
                
                if response.status_code != 200:
                    return {"error": f"Sarvam voice was unavailable."}
            
            res_data = response.json()
            if "audios" in res_data and res_data["audios"]:
                return {"audio_base64": f"data:audio/wav;base64,{res_data['audios'][0]}"}
            else:
                return {"error": "No audio returned from Sarvam API"}

    except Exception as e:
        log_event(f"Sarvam TTS Exception: {str(e)}")
        return {"error": "Server error in generating voice."}

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "brain": "Groq Llama-3",
        "voice": "Sarvam (Shruti/Meera)",
        "port": 8016
    }

@app.post("/feedback")
async def feedback(data: dict):
    """
    Captures explicit user feedback (Step 11).
    """
    log_event(f"FEEDBACK RECEIVED: {data}")
    # In a real app, this would update technique weights in the DB
    return {"status": "success", "message": "Feedback received"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8016, reload=False)
