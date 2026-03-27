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
        voice_tone = data.get("voice_tone", None)  # Voice tone from frontend
        detected_lang = data.get("detected_lang", "en")  # User's detected language
        
        # Log signals
        if emotion_data:
            log_event(f"Signals Received - Emotion: {emotion_data.get('emotion')}, Confidence: {emotion_data.get('score')}")
        if voice_tone:
            log_event(f"Voice Tone: {voice_tone}, Language: {detected_lang}")
        
        # Get session ID (default to 'global' if not provided)
        session_id = data.get("session_id", "default_user")
        if session_id not in session_history:
            session_history[session_id] = []
            
        # Step 2: Behavioral Analysis with History
        analysis = get_behavioral_analysis(message, emotion_data, session_history[session_id])
        
        # Add voice tone to analysis for frontend display
        analysis["voice_tone"] = voice_tone or "Unknown"
        analysis["user_lang"] = detected_lang
        
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
            return {"response": "I'm here, take your time.", "lang": "en-IN", "analysis": analysis}

        # Build face context string for LLM
        face_context = ""
        if emotion_data and emotion_data.get("emotion"):
            face_context = f"[FACE DETECTED: {emotion_data['emotion']} (confidence: {emotion_data.get('score', 0):.1f})]"

        # Adaptive language style based on detected user language
        lang_styles = {
            "ta": (
                "Respond in fluent Tanglish (English + Tamil). "
                "Examples: 'Arey enna achu da?', 'Parvaledu, we'll figure it out.', 'Romba stress ah irukku, let's try something.'"
            ),
            "te": (
                "Respond in fluent Telugulish (English + Telugu). "
                "Examples: 'Em ayindi ra?', 'Chala tough ga undi, I understand.', 'Parvaledu, relax avvu.'"
            ),
            "hi": (
                "Respond in fluent Hinglish (English + Hindi). "
                "Examples: 'Kya hua yaar?', 'Bahut tough lag raha hai, I get it.', 'Theek hai, let's try something.'"
            ),
            "en": (
                "Respond in warm, casual English with occasional South-Indian flavor. "
                "Examples: 'That sounds really heavy, you know...', 'Parvaledu, we got this.'"
            ),
        }
        lang_instruction = lang_styles.get(detected_lang, lang_styles["en"])

        # Adaptive tone based on voice tone
        tone_instruction = ""
        if voice_tone:
            tone_map = {
                "Agitated": "The user sounds agitated/frustrated. Be extra calm and grounding. Don't match their energy — be the anchor.",
                "Low / Subdued": "The user sounds low and subdued. Be extra warm and gentle. Speak softly, validate their pain.",
                "Anxious / Restless": "The user sounds anxious. Be reassuring and steady. Guide them to slow down.",
                "Upbeat": "The user sounds upbeat! Match their positive energy. Celebrate with them.",
                "Expressive": "The user is being expressive. Engage warmly and mirror their enthusiasm.",
                "Steady": "The user sounds calm and steady. Be conversational and natural.",
            }
            tone_instruction = tone_map.get(voice_tone, "")

        system_prompt = (
            "You are Theraπ — a warm, emotionally intelligent guide. "
            "YOUR ROLE: Help users understand what they're feeling and gently guide them through it. "
            "You are NOT a doctor. You are NOT a generic chatbot. You are a caring friend who knows mental wellness techniques. "
            "\n\nRULES (STRICT): "
            "1. NEVER say 'Hi', 'Hello', or any greeting. Jump straight into the conversation. "
            "2. Be CONCISE: 1-3 sentences MAX. This is a CONVERSATION, not a lecture. "
            f"3. LANGUAGE: {lang_instruction} "
            "   NEVER use pure Tamil/Telugu/Hindi paragraphs. Always mix with English naturally. "
            "4. USE CONTEXT IN YOUR REPLY — don't ignore what the engine detected: "
            f"   - The user's FACE looks: {emotion_data.get('emotion', 'unknown') if emotion_data else 'not visible'}. "
            f"   - Their VOICE TONE is: {voice_tone or 'not detected'}. "
            f"   - Engine classified their STATE as: {analysis['state']}. "
            "   Weave this naturally into your reply. Examples: "
            "   'I can see you're looking a bit tense...', 'Your voice sounds heavy today, you know...', "
            "   'Looks like there's some anxiety building up, no?'. "
            "   DON'T just say 'I sense' or 'I detect' — be natural about it. "
            "5. ACTIVELY guide them through the technique — don't just mention it. "
            f"   The recommended technique is: {analysis['selected_technique']}. "
            "   Walk them through it step-by-step in 1-2 sentences. "
            "   Example: If technique is 'Box Breathing', say: 'Let's breathe together — inhale 4 seconds... hold 4... exhale 4... ready?' "
            "   Example: If technique is 'Grounding (5-4-3-2-1)', say: 'Quick thing — tell me 5 things you can see right now?' "
            "6. If things seem serious, gently suggest professional help without scaring them. "
            "7. Be interruptible — keep responses SHORT so the user can jump in anytime. "
            f"\n\nTONE GUIDANCE: {tone_instruction} "
            f"\n\nENGINE CONTEXT (use this to ground your reply): "
            f"Detected State: {analysis['state']} | Risk Level: {analysis['risk_score']:.2f} | "
            f"Recommended Technique: {analysis['selected_technique']} | "
            f"Multimodal Confidence: {analysis['confidence_score']:.2f} | "
            f"Voice Tone: {voice_tone or 'N/A'} "
            "\n\nJSON response format: {\"response\": \"your message here\", \"lang\": \"en-IN\"}"
        )

        # Build the user message with multimodal context
        user_message = message
        if face_context:
            user_message = f"{face_context} User says: {message}"
        
        try:
            client = get_groq_client()
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
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
