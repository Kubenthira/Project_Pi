🧠 MindfulAI — Product Requirements Document (PRD) for Web Application
Voice-First, Behavior-Aware AI Companion for Mental Wellness — Web App Edition
Right Technique · Right Time · Minimal Intervention
This document is an updated version of the original MindfulAI PRD, changing the primary client from a Flutter mobile app to a web application while preserving the core product philosophy, decision loop, and AI stack.[1]
________________________________________
1. Executive Summary
MindfulAI is a voice-first, behavior-aware AI companion built for the Indian mental wellness market, now delivered primarily as a responsive web application accessible from any modern browser on mobile or desktop.[1]
Unlike generic chatbots that dump motivational quotes or long lectures, MindfulAI delivers one precise therapeutic micro-technique at exactly the right moment, grounded in CBT, mindfulness, and behavioral activation science.[1]
Core Philosophy
"Right technique, right time, minimal intervention" — not random tips, not stacked suggestions, but one targeted micro-intervention per turn.[1]
What Makes It Different
MindfulAI runs a transparent 12-step behavioral decision loop for every interaction: Signal Processing → Risk Scoring → Confidence Scoring → Clarification (if needed) → State Classification → Technique Selection → Safety Check → Delivery → Feedback → Learning.[1]
The system is designed as a decision-driven behavioral intervention engine that can be explained, audited, and continuously improved, rather than a black-box chatbot.[1]
________________________________________
2. Problem Statement
2.1 User-Side Crisis
India faces a large unmet need in mental health support, with tens of millions requiring help and only a small fraction having access to professional services.[1]
Therapy remains unaffordable for many students and early-career professionals, and stigma still discourages people from seeking formal treatment, despite their willingness to talk to their phones late at night when overwhelmed.[1]
2.2 Why Existing Solutions Fail
Key gaps in current tools include:
	Generic chatbots that ignore interaction history and behavioral patterns, effectively starting from zero each time.[1]
	Heavy, tasky apps that overload users with modules, tests, and long-form content, leading to churn within weeks.[1]
	Clinical vs. motivational mismatch, where apps are either too sterile and hospital-like or too superficial and "think positive" in tone.[1]
	No timing intelligence, since most solutions only respond when pinged and cannot optimize when to intervene.[1]
	No decision transparency, with pure text generation and no visible risk/confidence assessment.[1]
	Poor India language fit, especially for Hinglish, Tanglish, and Indian accents.[1]
2.3 The Gap MindfulAI Fills
The gap is not another chatbot; it is a decision-driven behavioral intervention system that knows when to speak, what to say, and how to learn from each interaction.[1]
The web application form factor removes installation friction and makes it easier for users to try MindfulAI instantly on mobile browsers and desktops.[1]
________________________________________
3. Market Analysis
3.1 Market Size & Growth
The Indian mental health app market and global mental wellness space are growing rapidly, with mental health/emotional support identified as one of the fastest-growing application segments for voice-based AI companions.[1]
MindfulAI is positioned at the intersection of mental health apps, voice-based AI companions, and behavioral health SaaS, with an India-first focus.[1]
3.2 Target Segment
Primary persona: "Stressed Aarav" — 18–35-year-old students and early-career professionals in Tier 1–3 Indian cities, comfortable with smartphones, voice notes, and code-mixed speech like Hinglish or Tanglish.[1]
Pain points include late-night overthinking, work stress, exam pressure, and relationship struggles, often expressed in informal, mixed-language speech rather than formal English.[1]
3.3 Target Use Cases
Typical scenarios:
	Late-night overthinking (11 PM–2 AM) → CBT reframing.[1]
	Post-work burnout → grounding or micro-reset routines.[1]
	Pre-exam panic → brief breathing exercises.[1]
	Relationship conflict → validation plus light guidance.[1]
	Monday morning dread → behavioral activation.[1]
3.4 Market Entry Strategy
The web application model enables frictionless trials via shareable links and QR codes, complementing campus and community-based acquisition strategies already planned for MindfulAI.[1]
________________________________________
4. Solution Overview
4.1 What MindfulAI Is
MindfulAI is a decision-driven behavioral intervention system, delivered as a responsive web app that:
	Listens to voice in real time (Indian languages + code-mixed speech).
	Extracts sentiment, emotion, and distress phrases.
	Computes a Risk Score and Confidence Score between 0 and 1.
	Optionally asks a clarification question when confidence is low.
	Classifies the user's current mental state.
	Selects one primary therapeutic technique.
	Generates a short, safe, validating response.
	Delivers the response as voice plus synced text in the browser.
	Captures explicit and implicit feedback.
	Learns which techniques work best for that user over time.[1]
4.2 What MindfulAI Is Not
MindfulAI is therapy-informed, not therapy-replacing: it does not diagnose, prescribe, or claim to replace human therapists, and it always escalates crisis situations to verified helplines rather than attempting to handle them autonomously.[1]
Raw audio is not stored; only processed text and derived signals are retained, with strong privacy controls and the ability for users to delete their data.[1]
4.3 Core Design Rules
Core design principles include:
	One-Technique Rule: at most one main technique per interaction turn.
	Validation-First Rule: always acknowledge the user's emotion before suggesting anything.
	Timing Over Intelligence: simple and timely beats complex and late.
	Minimalism Rule: short, concrete responses and 1–3 minute exercises.
	Adaptive Behavior: per-user technique preferences evolve from feedback, without long preference surveys.[1]
________________________________________
5. Detailed Product Behavior — The 12-Step Loop
MindfulAI’s heart is a 12-step behavioral decision loop that processes each interaction from input to learning.[1]
The loop encompasses input collection, signal extraction, risk and confidence scoring, optional clarification, state classification, technique selection, intervention generation, safety checking, delivery, feedback, and long-term adaptation.[1]
Key components:
	Input Collection: voice (mandatory), optional text, and recent history.[1]
	Signal Processing: sentiment, emotion indicators, and distress keywords.[1]
	Risk Scoring: computes risk_score ∈ 0,1 and triggers crisis escalation when above threshold.[1]
	Confidence Scoring: evaluates statement clarity and pattern consistency to decide if clarification is needed.[1]
	Clarification Engine: asks a single empathetic clarifying question when confidence is low.[1]
	State Classification: categorizes into states like overthinking, anxiety, fatigue, low motivation, negative self-talk, or emotional distress.[1]
	Technique Selection: maps states to primary and fallback techniques (e.g., CBT reframing, breathing, grounding, behavioral activation, validation).[1]
	Intervention Generation: follows a three-part structure — validation, technique, and follow-up.[1]
	Trust/Safety Check: a dedicated safety pass ensures no medical claims, unsafe instructions, or invalidating tone.[1]
	Response Delivery: voice output plus text transcript.[1]
	Feedback Loop: explicit yes/no feedback and implicit signals like engagement and sentiment shift.[1]
	Learning & Adaptation: updates technique weights and thresholds, driving personalization.[1]
________________________________________
6. Technology Stack — Web Application First
6.1 Overview
MindfulAI uses a modern web-based stack: a Next.js web client, a FastAPI backend orchestrating a Sarvam AI stack, and Firebase/Supabase for data and auth.[1]
The shift from Flutter to web focuses on rapid access, easier distribution, and shared infrastructure between the marketing site and the app shell.[1]
6.2 Client — Web Application (Next.js)
Component	Technology	Justification
Framework	Next.js (React)	Single codebase for desktop and mobile web; SSR for SEO; excellent performance.
Rendering	Next.js App Router + SSR/ISR	SEO-friendly for public pages, fast navigation for app flows.
UI Library	Tailwind CSS + Headless UI	Rapid UI development; consistent design system; responsive layout.
Audio Capture	Web Audio API + getUserMedia	Low-latency mic access directly in the browser; no native app install required.
Audio Streaming	WebSocket (Browser WebSocket API)	Real-time audio chunk streaming to backend orchestrator.
State Management	React Query / Zustand	Predictable state handling for conversation flow and cached data.
Routing	Next.js App Router	Clean separation between marketing pages, auth, and app area (/app).
Auth Integration	Firebase Auth JS SDK	Phone OTP, email, Google login in-browser; minimal friction.
Offline Support	Service Worker / IndexedDB	Cache recent sessions and preferences; tolerate flaky mobile data.

6.3 Client — Marketing Website (Next.js)
The marketing website shares the same Next.js codebase, reusing components and styling for consistency.[1]
It uses Tailwind CSS and MDX for content, and is hosted on Vercel for zero-config deployment, previews, and global CDN caching.[1]
6.4 Backend — API & Orchestration
The backend continues to use Python FastAPI as the primary framework, with WebSocket support for real-time audio streaming and optional task queues (Celery + Redis) for background jobs.[1]
Deployment targets include Google Cloud Run or similar serverless container platforms, enabling auto-scaling and pay-per-use economics.[1]
6.5 AI & APIs — Sarvam AI Stack
The AI layer integrates:
	Saaras STT for streaming speech-to-text in Indian languages and code-mixed speech.
	Sarvam Chat LLM for signal extraction, classification, technique selection, and response templating.
	Bulbul TTS for high-quality Indian voices in Hindi, Tamil, and Indian-accent English.[1]
These India-first models provide superior UX compared to generic global STT/TTS for the target demographic.[1]
6.6 Data & Storage
Core components include:
	Primary Database: Firestore or Supabase for real-time sync and simple integration with the web client.
	Authentication: Firebase Auth for phone, email, and social logins.
	Analytics: Firebase Analytics with custom events to track engagement and technique effectiveness.
	File Storage: optional Firebase Storage for future user-uploaded context.[1]
6.7 Development Tooling
Development may use agentic coding tools to scaffold backend, infrastructure, and UI code, plus test synchronization and pair-programming workflows.[1]
________________________________________
7. System Architecture — Web Client
7.1 High-Level Architecture
The high-level architecture remains: Web Client → API Gateway → Conversation Orchestrator → Sarvam Services → Database, with the client now being a browser-based app instead of a Flutter mobile client.[1]
The architecture supports streaming audio, live captions, decision logic, and feedback-driven learning.
7.2 Logical Components — Detailed
🌐 Web Client (Browser App)
	Audio Capture: uses Web Audio API and getUserMedia to capture mic audio, sending encoded chunks over WebSocket.
	Live Captions: receives partial/final STT transcripts and updates the UI in real time.
	Conversation UI: chat-style timeline showing user utterances (text transcripts) and AI responses (text + play/pause audio controls).
	Feedback Controls: inline "Did that help?" yes/no buttons, emoji reactions, and optional text feedback.
	Insights View: weekly summaries of mood trends, techniques, and helpfulness scores.
	Responsive Layout: mobile-first design for smooth experience on Android and iOS browsers.
🚪 API Gateway / Orchestrator
The gateway handles auth verification, rate limiting, and routing of WebSocket streams and HTTP requests to the conversation orchestrator and behavioral engine.[1]
🎛️ Conversation Orchestrator
Implements the 12-step decision loop, coordinating STT, LLM processing, risk/confidence logic, technique selection, safety checks, TTS, and feedback handling.[1]
📊 Behavioral Engine
Computes behavioral patterns such as late-night usage, withdrawal, and repeated negativity, and generates simple insights for users.[1]
💊 Intervention Engine
Manages the technique library, mapping logic, response templates, and effectiveness scoring per user.[1]
7.3 Example Request Flow (Web)
The sequence is conceptually identical to the mobile version, with the client now labeled "🌐 User (Web App – Browser)":
	User → Gateway: audio stream via WebSocket.
	Gateway → Orchestrator: forward audio chunks.
	Orchestrator → Saaras: streaming STT request.
	Saaras → Orchestrator: transcripts.
	Orchestrator → Web Client: live captions.
	Orchestrator → LLM: signals and classification.
	LLM → Orchestrator: state, risk, confidence, technique recommendations.
	Orchestrator → LLM: intervention generation.
	LLM → Orchestrator: validated response text.
	Orchestrator → Bulbul: TTS request.
	Bulbul → Orchestrator: audio buffer.
	Orchestrator → Web Client: audio + text response.
	User → Gateway: explicit feedback.
	Gateway/Orchestrator → DB: persist session, feedback, and updated scores.[1]
________________________________________
8. Data Model & Schema
The data model remains centered around users, sessions, messages, interventions, behavioral patterns, and state snapshots, with fields such as technique weights, risk/confidence scores, and derived insights.[1]
All collections are stored in Firestore or Supabase with strict access control and encryption in transit and at rest.[1]
________________________________________
9. API Contract & Integration Points
The HTTP and WebSocket API surface remains:
	Session Management: start, end, and history endpoints.
	Real-time Conversation (WebSocket): client sends audio chunks, server streams transcripts and response messages.
	Feedback: explicit feedback submission endpoint.
	Insights: daily and weekly insight endpoints.[1]
Sarvam integration points map cleanly onto backend services for STT, LLM, and TTS.[1]
________________________________________
10. Security, Privacy & Compliance
The privacy architecture enforces:
	Encryption at rest and in transit.
	Access control so users can only access their own data.
	No storage of raw audio; only transcripts and derived metadata.
	GDPR/DPDPA-style rights including account and data deletion on request.[1]
Safety protocols define clear responses for high risk scores, self-harm keywords, medical advice requests, repeated high-risk sessions, and data deletion requests.[1]
________________________________________
11. Competitive Analysis & USPs
MindfulAI’s competitive differentiation remains:
	Voice-first, India-language-first UX (Hinglish, Tanglish, Hindi, Tamil).
	Transparent decision loop with explicit risk and confidence scoring.
	Timing intelligence and behavioral patterns.
	Minimalist, one-technique-per-turn interventions.
	Strong safety and trust layer.
	Web-based delivery, reducing install friction and broadening reach.[1]
________________________________________
12. Go-to-Market Strategy — Web Focus
The go-to-market plan now emphasizes:
	Zero-friction access via a public web URL and PWA-style experience.
	Campus and community partnerships where QR codes and short links drive users to the web app.
	Social content (reels, posts) linking directly to the web app.
	Product Hunt and similar launches where browser-based access is an advantage.[1]
________________________________________
13. Phased Roadmap (Platform-Specific)
Phase 1 (Months 1–3) — MVP Web App
	Responsive web app (Next.js) with browser mic input.
	FastAPI backend with WebSocket support.
	Sarvam STT integration (Hinglish first).
	Core 12-step loop (at least input → delivery).
	Basic state classification (initial set of states).
	Three technique types (breathing, CBT reframing, validation).
	Sarvam TTS output (Hindi voice).
	Firebase Auth (phone OTP).
	Firestore data storage.
	Basic explicit feedback collection.
Phase 2 (Months 4–6) — Enhanced Experience
	Full 12-step loop with learning and adaptation.
	All six state classifications and five technique types.
	Behavioral engine for pattern detection.
	Weekly insights web dashboard.
	Implicit feedback tracking.
	Tamil and Indian English support.
	PWA optimization (home-screen install, offline shell).
	Public production web launch.
Phase 3+ — Scale and Optional Native Wrappers
	Optional native wrappers (Android/iOS via Capacitor or similar) that host the web app for users who prefer store installs.
	Campus dashboards for partners.
	Advanced personalization, voice tone analysis, proactive interventions, and A/B testing.
	Premium subscription tier and B2B offerings.[1]
________________________________________
14. Risk Assessment & Mitigation (Web-Specific Considerations)
Key risks include:
	Browser permission friction for mic access → mitigated by clear onboarding and UX copy.
	Network reliability for real-time streaming → mitigated by graceful degradation and reconnect logic.
	Device variability across mobile browsers → mitigated by responsive design and cross-browser testing.
	Privacy concerns in shared devices/browsers → mitigated by explicit logout, minimal local storage, and clear privacy education.[1]
________________________________________
15. Success Metrics & KPIs
Success metrics remain centered on:
	Weekly active users.
	Session frequency per user.
	Average session duration.
	Sentiment shift within sessions.
	Technique effectiveness scores.
	Retention and habit formation indicators.[1]
________________________________________
16. Team Structure & Roles (Updated Client Role)
Key roles include:
	Product Lead — owns PRD, roadmap, and user research.
	Web Frontend Developer (React/Next.js) — builds the web app UI, audio capture, and WebSocket integration.
	Backend Engineer (FastAPI) — implements APIs, orchestrator, and Sarvam integration.
	AI/ML Engineer — designs signal-processing pipeline, classification, and personalization.
	Design — leads UX, UI, and conversation design.
	QA/Safety — covers quality, regression, and safety testing with mental health-informed scenarios.[1]
________________________________________
17. Summary
This PRD repositions MindfulAI as a web-first, voice-first AI companion while preserving the original behavioral architecture and India-focused AI stack.[1]
The web application approach optimizes for accessibility, rapid experimentation, and broad reach across devices, aligning with hackathon timelines and early-stage product validation needs.[1]
________________________________________
