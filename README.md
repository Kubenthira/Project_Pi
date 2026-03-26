# Mental Health Companion AI 🧠💖

## 🌟 Overview
The **Mental Health Companion AI** is a compassionate digital assistant designed to provide emotional support and comfort. Built with modern AI technologies, it serves as a supportive listener that identifies user feelings and offers empathetic responses in real-time.

### 🧘 The Mission
In a world where mental well-being is increasingly important, this project provides a safe, accessible space for users to express themselves. Our goal is to offer comfort and validation through a friendly, interactive 3D avatar that feels personal and responsive.

### 🛡️ Our Approach: "Comfort, Not Diagnosis"
- **Identify & Comfort**: The AI is programmed to recognize emotional cues and respond with empathy.
- **Non-Diagnostic**: Strictly avoids clinical diagnosis or medical advice. It is a companion, not a replacement for professional therapy.
- **Native Experience**: Responds in the user's preferred language to ensure deep connection and accessibility.

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
