# Mental Health Companion AI 🧠💖

A supportive, empathetic AI avatar built with Three.js, Groq (Llama-3), and Sarvam AI. This companion identifies your feelings and provides comfort without diagnosing, always responding in your own language.

## ✨ Features
- **Empathetic Companion**: Powered by Groq Llama-3, specifically tuned for supportive mental health interactions.
- **Multi-language Support**: Automatically detects and responds in **Tamil (ta-IN)**, **Telugu (te-IN)**, **Hindi (hi-IN)**, and **English (en-IN)**.
- **Premium Voice**: High-quality TTS using Sarvam AI (Shruti/Meera).
- **Interactive Avatar**: Features a 3D VRM model with real-time expression blending based on emotions.
- **Premium Design**: Modern UI with glassmorphism and responsive layout.

---

## 🚀 Quick Start (Local Setup)

This project consists of a FastAPI backend proxy and a static frontend.

### 1. Prerequisites
- Python 3.10+
- A `.env` file in the root directory with the following keys:
  ```env
  GROQ_API_KEY=your_key_here
  SARVAM_API_KEY=your_key_here
  ```

### 2. Run the Backend (FastAPI)
The backend handles the Groq brain and Sarvam voice engine.
```powershell
.\.venv\Scripts\python.exe face_detection.py
```
*Runs on [http://localhost:8016](http://localhost:8016)*

### 3. Run the Frontend (Static Server)
Host the `index.html` interface.
```powershell
.\.venv\Scripts\python.exe -m http.server 8001
```
*Access via [http://localhost:8001/index.html](http://localhost:8001/index.html)*

---

## 📂 Architecture
- **Brain**: [Groq](https://groq.com) (Llama-3.1-8b-instant)
- **Voice**: [Sarvam AI](https://www.sarvam.ai) (Bulbul:v3)
- **Avatar**: Three.js VRM Loader
- **Emotion**: Face-api.js (Browser-based detection)

---

## 🛠️ Folder Structure
```text
FINAL/
├── face_detection.py  # FastAPI Backend (Proxy)
├── index.html         # Main application (Frontend)
├── .env               # API Configuration
├── README.md          # Documentation
└── [model].vrm        # 3D Avatar Model
```
