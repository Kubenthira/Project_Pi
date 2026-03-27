# 🧠 Theraπ (Project Pi) — Product Requirements Document

**Voice-First, Behavior-Aware AI Companion for Mental Wellness**
*Right Technique · Right Time · Minimal Intervention*

---

## 1. Executive Summary

Theraπ is a **voice-first, behavior-aware AI companion** for mental wellness, delivered as a web application featuring a **3D VRM avatar** with real-time emotion-driven facial expressions, a **heuristic behavioral scoring engine**, and **adaptive multilingual responses**.

Unlike generic chatbots, Theraπ runs a transparent behavioral decision loop for every interaction — processing multimodal signals (text + face + voice tone), computing risk and confidence scores via a **non-LLM heuristic engine**, classifying the user's mental state, selecting one targeted therapeutic technique, and generating a short, empathetic response in the user's preferred language style.

### Core Philosophy

> *"Right technique, right time, minimal intervention"* — not random tips, not stacked suggestions, but **one targeted micro-intervention per turn**.

### What Makes It Different

| Feature | Theraπ | Generic Chatbots |
|---|---|---|
| Decision-making | Heuristic engine (non-LLM) | LLM decides everything |
| Multimodal input | Face + Text + Voice Tone | Text only |
| Language | Adaptive Tanglish/Telugulish/Hinglish | English only |
| Persona | Warm Guide (observation-first) | Generic "Hi, how can I help?" |
| Transparency | Real-time engine trace tiles | Black box |
| Avatar | 3D VRM with emotion-synced expressions | Text or 2D |

---

## 2. Problem Statement

### 2.1 User-Side Crisis
- India has a massive unmet mental health need (tens of millions) with minimal professional access
- Therapy is unaffordable for most students and early-career professionals
- Stigma discourages formal help-seeking, but users are willing to talk to their phones late at night

### 2.2 Why Existing Solutions Fail
- **Generic chatbots** ignore behavioral patterns and start from zero each time
- **Heavy apps** overload users with modules, tests, and long-form content → churn within weeks
- **No timing intelligence** — most only respond when pinged
- **No decision transparency** — pure text generation with no visible risk/confidence assessment
- **Poor India language fit** — fail with Hinglish, Tanglish, and Indian accents

### 2.3 The Gap Theraπ Fills
A **decision-driven behavioral intervention system** that knows when to speak, what to say, and adapts to the user's language, tone, and emotional state in real time.

---

## 3. Target Audience

**Primary Persona: "Stressed Aarav"**
- 18–35 year-old students and early-career professionals
- Tier 1–3 Indian cities
- Comfortable with voice notes and code-mixed speech (Hinglish/Tanglish)
- Pain points: late-night overthinking, work stress, exam pressure, relationship struggles

**Target Use Cases:**
| Scenario | Technique |
|---|---|
| Late-night overthinking (11 PM–2 AM) | CBT Reframing |
| Post-work burnout | Grounding (5-4-3-2-1) |
| Pre-exam panic | Box Breathing (4-7-8) |
| Relationship conflict | Empathetic Validation |
| Monday morning dread | Behavioral Activation |
| Loneliness/isolation | Cognitive Defusion |
| Anger/frustration | Progressive Muscle Relaxation |

---

## 4. Current Architecture (As Built)

### 4.1 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Vanilla HTML/CSS/JS | Single-page web app |
| **3D Avatar** | Three.js + VRM Loader | Emotion-synced 3D character |
| **Face Detection** | face-api.js (TinyFaceDetector) | Real-time webcam emotion detection |
| **Speech-to-Text** | Web Speech API (SpeechRecognition) | Browser-native voice input |
| **Backend** | Python FastAPI + Uvicorn | API orchestration |
| **Scoring Engine** | Custom Python heuristics (`scoring.py`) | Risk/State/Technique — NO LLM |
| **LLM (Response Only)** | Groq API (LLaMA 3.1 8B Instant) | Empathetic response generation |
| **Text-to-Speech** | Sarvam AI (Bulbul TTS) | Indian-voice audio output |
| **Hosting** | Vercel (Frontend) + Local/Cloud (Backend) | Deployment |

### 4.2 File Structure

```
Project_Pi/
├── index.html          # Full frontend (3D avatar, chat, trace tiles, webcam)
├── api.py              # FastAPI backend (orchestration, LLM proxy, TTS proxy)
├── scoring.py          # Heuristic behavioral engine (risk, state, technique)
├── requirements.txt    # Python dependencies
├── .env                # API keys (GROQ_API_KEY, SARVAM_API_KEY)
├── prd.md              # This document
└── .venv/              # Python virtual environment
```

---

## 5. Behavioral Decision Loop (As Implemented)

### 5.1 Overview

Every user interaction triggers a **6-step heuristic decision loop** — entirely in `scoring.py`, with **zero LLM involvement** for classification.

```
User Input (Text + Face + Voice Tone)
        ↓
┌─────────────────────────────────┐
│ Step 1: Signal Processing       │  Extract text keywords + face emotion + voice tone
│ Step 2: Risk Scoring            │  Weighted lexicon + sigmoid normalization
│ Step 3: Confidence Scoring      │  Multimodal alignment (text ↔ face)
│ Step 4: State Classification    │  Priority-ordered rules (9 states)
│ Step 5: Technique Selection     │  State → Technique mapping
│ Step 6: Trend Detection         │  Session history pattern analysis
└─────────────────────────────────┘
        ↓
Analysis Result (risk_score, confidence_score, state, technique, is_trend)
        ↓
LLM generates empathetic response GUIDED BY the analysis
        ↓
Sarvam TTS speaks the response
```

### 5.2 Scoring Engine Details (`scoring.py`)

#### Weighted Distress Lexicon
- **40+ keywords** with clinical severity weights (0.05–0.9)
- Categories: Crisis (kill, suicide, end it → 0.7–0.9), Anxiety (anxious, panic → 0.4–0.5), Depression (hopeless, worthless → 0.5–0.6), Stress (stressed, overwhelmed → 0.3–0.4), Mild distress (tired, bored → 0.05–0.15)

#### Positive Signal Lexicon
- **18 keywords** that actively reduce risk score (happy, grateful, peaceful, etc.)

#### Risk Score Calculation
```
raw_score = Σ(keyword_weight) - Σ(positive_weight × 0.3)
risk_score = sigmoid(raw_score) ∈ [0.0, 1.0]
```

#### Multimodal Confidence Score
- Measures **alignment** between text sentiment and face emotion
- High confidence when text and face agree (e.g., "I'm sad" + sad face = 0.95)
- Low confidence when they conflict (e.g., "I'm fine" + sad face = 0.65)

#### State Classification (9 States, Priority-Ordered)

| Priority | State | Primary Trigger |
|---|---|---|
| 1 | Crisis / Immediate Risk | Crisis keywords (kill, suicide) |
| 2 | Anxiety / Panic | Anxiety keywords + fearful face |
| 3 | Depression / Deep Sadness | Depression keywords + sad face |
| 4 | Fatigue / Burnout | Exhaustion keywords |
| 5 | Overthinking / Rumination | Overthinking patterns |
| 6 | Frustration / Anger | Anger keywords + angry face |
| 7 | Loneliness / Isolation | Loneliness keywords |
| 8 | Stress / Pressure | Stress keywords |
| 9 | Positive / Upbeat | Happy/grateful signals |
| Default | General Reflection | No specific signals |

#### Technique Mapping

| State | Primary Technique |
|---|---|
| Crisis | Safety Protocol → Helpline Escalation |
| Anxiety / Panic | Box Breathing (4-7-8 Technique) |
| Depression | Behavioral Activation + Gratitude Journaling |
| Fatigue / Burnout | Micro-Rest (2-Min Body Scan) |
| Overthinking | CBT Thought Record (Catch → Check → Change) |
| Frustration / Anger | Progressive Muscle Relaxation |
| Loneliness | Cognitive Defusion + Social Reconnection |
| Stress / Pressure | Grounding (5-4-3-2-1 Technique) |
| Positive | Gratitude Amplification |
| General | Empathetic Validation |

---

## 6. AI Persona — Theraπ

### 6.1 Personality Profile

Theraπ is a **Warm Guide** — not a doctor, not a generic chatbot. A caring friend who understands mental wellness techniques.

**Key Traits:**
- **Observation-first:** Never starts with "Hi/Hello." Jumps straight into what the user seems to be feeling.
- **Concise:** 1–3 sentences max. This is a conversation, not a lecture.
- **Proactive:** Actively guides users through techniques instead of just mentioning them.
- **Interruptible:** Keeps responses short so the user can jump in anytime.

### 6.2 Adaptive Language

The AI dynamically adapts its language based on the user's detected language:

| User Language | AI Response Style | Example |
|---|---|---|
| Tamil | Tanglish (English + Tamil) | "Arey enna achu da? Let's try something together..." |
| Telugu | Telugulish (English + Telugu) | "Em ayindi ra? Chala tough ga undi, I understand..." |
| Hindi | Hinglish (English + Hindi) | "Kya hua yaar? Bahut tough hai, let's breathe..." |
| English | Warm casual English | "That sounds heavy... Parvaledu, we got this." |

**STRICT RULE:** Never pure Tamil/Telugu/Hindi paragraphs. Always mixed naturally with English.

### 6.3 Adaptive Tone

Based on the detected voice tone, the AI adapts its emotional delivery:

| Detected Tone | AI Behavior |
|---|---|
| Agitated | Extra calm and grounding — be the anchor |
| Low / Subdued | Extra warm and gentle — validate the pain |
| Anxious / Restless | Reassuring and steady — guide them to slow down |
| Upbeat | Match positive energy — celebrate with them |
| Expressive | Engage warmly — mirror their enthusiasm |
| Steady | Conversational and natural |

### 6.4 Response Pattern

```
1. Name the state: "Sounds like you're carrying a lot of frustration, no?"
2. Validate: "That's completely understandable, yaar..."
3. Guide through technique: "Let's breathe together — inhale 4 seconds... hold 4... exhale 4... ready?"
```

---

## 7. Frontend UI — Distributed Engine Trace

### 7.1 Layout

```
┌──────────────────────────────────────────────────────┐
│  [Engine Trace Tiles]          [3D Avatar]    [Webcam]│
│  📡 Signal: HAPPY (0.87)       ┌─────────┐   ┌─────┐│
│  ⚡ Risk: 0.119 (green)        │         │   │ YOU ││
│  🧠 State: Positive/Upbeat    │  Theraπ │   │     ││
│  💊 Strategy: Gratitude Amp    │  (VRM)  │   └─────┘│
│  🎙️ Voice: Steady (English)    │         │   [Chat] │
│                                └─────────┘   │     ││
│                                              │     ││
│                                              └─────┘│
└──────────────────────────────────────────────────────┘
```

### 7.2 Trace Tiles (Left Side)

| Tile | Content | Update Frequency |
|---|---|---|
| 📡 Input Signal | Face emotion + confidence | Real-time (200ms) |
| ⚡ Risk Score | 0.000–1.000, color-coded | Per chat response |
| 🧠 State Classification | Detected mental state tag | Per chat response |
| 💊 Strategy | Selected therapeutic technique | Per chat response |
| 🎙️ Voice Tone | Detected voice tone + language | Per voice input |

### 7.3 Visual Risk Feedback

The chat container dynamically glows based on the current risk level:
- 🟢 **Green glow** (risk < 0.3) — Safe
- 🟡 **Amber glow** (risk 0.3–0.6) — Alert
- 🔴 **Red pulse** (risk > 0.6) — High risk, pulsing animation

### 7.4 3D Avatar

- **Model:** VRM format, loaded via `@pixiv/three-vrm`
- **Expressions:** Emotion-synced (happy, sad, angry, surprised, neutral) via VRM expression system
- **Lip Sync:** Audio-driven mouth movement during TTS playback
- **Framing:** Shoulder-up, centered in the viewport

---

## 8. Multimodal Input Pipeline

### 8.1 Signal Sources

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  Webcam      │    │  Microphone   │    │  Text Input   │
│  (face-api)  │    │  (Web Speech) │    │  (keyboard)   │
└──────┬──────┘    └──────┬───────┘    └──────┬────────┘
       │                  │                    │
       ▼                  ▼                    ▼
  Face Emotion      Voice Tone +           Raw Text
  + Confidence      Language Detection
       │                  │                    │
       └──────────────────┼────────────────────┘
                          ▼
              ┌─────────────────────┐
              │   scoring.py        │
              │   (Heuristic Engine)│
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │   Groq LLM          │
              │   (Response ONLY)   │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │   Sarvam TTS        │
              │   (Voice Output)    │
              └─────────────────────┘
```

### 8.2 Data Sent to Backend (`/chat` endpoint)

```json
{
  "text": "I'm feeling really stressed about exams",
  "emotion_data": {
    "emotion": "fearful",
    "score": 0.82
  },
  "voice_tone": "Anxious / Restless",
  "detected_lang": "en"
}
```

### 8.3 Backend Response

```json
{
  "response": "That exam pressure is real, yaar... Let's try something quick — breathe in for 4 seconds... hold... now exhale slowly. Ready?",
  "lang": "en-IN",
  "analysis": {
    "risk_score": 0.47,
    "confidence_score": 0.97,
    "state": "Anxiety / Panic",
    "selected_technique": "Box Breathing (4-7-8 Technique)",
    "is_trend": false,
    "voice_tone": "Anxious / Restless",
    "user_lang": "en",
    "input_signals": {
      "face_emotion": "fearful",
      "face_confidence": 0.82,
      "text_length": 43,
      "session_depth": 0
    },
    "engine_version": "2.0-heuristic"
  }
}
```

---

## 9. Safety & Ethics

### 9.1 Safety Circuit Breaker
- Risk score ≥ 0.8 triggers an **immediate safety response** with helpline numbers
- No LLM involvement in safety decisions — purely heuristic

### 9.2 What Theraπ Is NOT
- ❌ Not a replacement for therapy
- ❌ Does not diagnose or prescribe
- ❌ Does not store raw audio
- ❌ Does not make medical claims

### 9.3 Crisis Escalation
When crisis keywords are detected (suicide, self-harm, etc.), the system immediately provides:
- National helpline numbers (iCall, Vandrevala Foundation)
- Clear messaging that professional help is available
- No further AI interaction until user explicitly continues

---

## 10. Dependencies & Environment

### 10.1 Python Dependencies (`requirements.txt`)
```
fastapi
uvicorn
httpx
python-dotenv
groq
```

### 10.2 Environment Variables (`.env`)
```
GROQ_API_KEY=<your-groq-api-key>
SARVAM_API_KEY=<your-sarvam-api-key>
```

### 10.3 Running Locally
```bash
# Backend (port 8016)
python api.py

# Frontend (port 8001)
python -m http.server 8001
```

---

## 11. Design Principles

1. **Non-LLM Decisions:** The LLM generates responses only — all risk scoring, state classification, and technique selection is done by the heuristic engine.
2. **Transparency:** Every decision the engine makes is visible to the user via the trace tiles.
3. **One-Technique Rule:** At most one therapeutic technique per interaction turn.
4. **Validation-First:** Always acknowledge the user's emotion before suggesting anything.
5. **Minimalism:** Short, concrete responses. 1–3 sentences max.
6. **Adaptive Behavior:** Language and tone adapt to the user's input without configuration.
7. **Safety-First:** Crisis detection is heuristic-based and cannot be overridden by the LLM.
