import logging
import math

logger = logging.getLogger("MindfulAI-Scoring")

# ─────────────────────────────────────────────────────────────
# 1. WEIGHTED DISTRESS LEXICON
#    Each keyword carries a weight reflecting clinical severity.
# ─────────────────────────────────────────────────────────────
DISTRESS_LEXICON = {
    # Critical (weight 0.9)
    "suicide": 0.9, "kill myself": 0.9, "end it all": 0.9,
    "no reason to live": 0.9, "want to die": 0.9, "hurt myself": 0.85,
    "self harm": 0.85, "cutting myself": 0.85,
    # Severe (weight 0.5–0.7)
    "hopeless": 0.6, "worthless": 0.6, "i'm nothing": 0.65,
    "cannot go on": 0.6, "give up": 0.55, "no way out": 0.6,
    "breaking down": 0.55, "losing my mind": 0.55,
    "can't take it": 0.5, "done with everything": 0.55,
    "nobody cares": 0.5, "all alone": 0.5,
    # Moderate (weight 0.2–0.4)
    "anxious": 0.35, "panic": 0.4, "scared": 0.35,
    "terrified": 0.4, "overwhelmed": 0.35, "paranoid": 0.35,
    "depressed": 0.4, "miserable": 0.35, "numb": 0.3,
    "exhausted": 0.25, "burnout": 0.3, "burned out": 0.3,
    "frustrated": 0.25, "angry": 0.25, "furious": 0.3,
    "confused": 0.2, "lost": 0.2, "stuck": 0.2,
    "lonely": 0.3, "isolated": 0.3, "abandoned": 0.35,
    # Mild (weight 0.05–0.15)
    "sad": 0.15, "upset": 0.15, "unhappy": 0.15,
    "stressed": 0.12, "worried": 0.1, "nervous": 0.1,
    "tired": 0.08, "sleepless": 0.12, "restless": 0.1,
    "bored": 0.05, "irritated": 0.08, "annoyed": 0.08,
}

# ─────────────────────────────────────────────────────────────
# 2. POSITIVE SIGNAL LEXICON (reduces risk)
# ─────────────────────────────────────────────────────────────
POSITIVE_LEXICON = {
    "happy": 0.15, "great": 0.12, "amazing": 0.15, "wonderful": 0.12,
    "excited": 0.1, "grateful": 0.12, "thankful": 0.1,
    "good": 0.08, "better": 0.08, "okay": 0.05,
    "love": 0.1, "proud": 0.1, "confident": 0.08,
    "relaxed": 0.1, "calm": 0.1, "peaceful": 0.12,
    "motivated": 0.1, "energized": 0.08, "hopeful": 0.12,
}

# ─────────────────────────────────────────────────────────────
# 3. STATE CLASSIFICATION RULES (priority-ordered)
# ─────────────────────────────────────────────────────────────
STATE_RULES = [
    {
        "state": "Crisis / Immediate Risk",
        "text_signals": ["suicide", "kill myself", "end it all", "want to die", "no reason to live", "hurt myself", "self harm"],
        "face_signals": [],
        "min_risk": 0.7,
    },
    {
        "state": "Anxiety / Panic",
        "text_signals": ["panic", "anxious", "scared", "terrified", "can't breathe", "heart racing", "shaking", "paranoid"],
        "face_signals": ["fearful", "surprised"],
        "min_risk": 0.0,
    },
    {
        "state": "Depression / Low Mood",
        "text_signals": ["depressed", "hopeless", "worthless", "numb", "empty", "miserable", "no motivation"],
        "face_signals": ["sad"],
        "min_risk": 0.0,
    },
    {
        "state": "Fatigue / Burnout",
        "text_signals": ["exhausted", "burnout", "burned out", "tired", "drained", "sleepless", "no energy", "can't sleep"],
        "face_signals": ["neutral"],
        "min_risk": 0.0,
    },
    {
        "state": "Overthinking / Rumination",
        "text_signals": ["overthinking", "can't stop thinking", "stuck in my head", "looping", "what if", "always thinking", "racing thoughts"],
        "face_signals": [],
        "min_risk": 0.0,
    },
    {
        "state": "Frustration / Anger",
        "text_signals": ["frustrated", "angry", "furious", "annoyed", "irritated", "hate", "pissed"],
        "face_signals": ["angry", "disgusted"],
        "min_risk": 0.0,
    },
    {
        "state": "Loneliness / Isolation",
        "text_signals": ["lonely", "alone", "isolated", "nobody", "abandoned", "no friends", "nobody cares"],
        "face_signals": ["sad"],
        "min_risk": 0.0,
    },
    {
        "state": "Stress / Pressure",
        "text_signals": ["stressed", "overwhelmed", "pressure", "deadline", "too much", "can't handle"],
        "face_signals": [],
        "min_risk": 0.0,
    },
    {
        "state": "Positive / Upbeat",
        "text_signals": ["happy", "great", "amazing", "excited", "wonderful", "grateful", "proud", "love"],
        "face_signals": ["happy"],
        "min_risk": 0.0,
    },
]

# ─────────────────────────────────────────────────────────────
# 4. TECHNIQUE MAP (maps states to micro-interventions)
# ─────────────────────────────────────────────────────────────
TECHNIQUE_MAP = {
    "Crisis / Immediate Risk": "Safety Protocol → Helpline Escalation",
    "Anxiety / Panic": "Box Breathing (4-7-8 Technique)",
    "Depression / Low Mood": "Behavioral Activation (Micro-Win Strategy)",
    "Fatigue / Burnout": "5-4-3-2-1 Grounding Exercise",
    "Overthinking / Rumination": "CBT Cognitive Reframing",
    "Frustration / Anger": "Progressive Muscle Relaxation",
    "Loneliness / Isolation": "Self-Compassion Reflection",
    "Stress / Pressure": "Mindful Body Scan (60s)",
    "Positive / Upbeat": "Gratitude Amplification",
    "General Reflection": "Empathetic Validation",
    # Trend overrides
    "Persistent Anxiety Pattern": "Deep Grounding + Professional Referral",
    "Chronic Fatigue Pattern": "Energy Pacing Strategy",
    "Recursive Thought Loop": "Thought-Stopping Visualization",
    "Escalating Frustration": "Cool-Down Protocol + Journaling Prompt",
}


# ═════════════════════════════════════════════════════════════
# SCORING FUNCTIONS
# ═════════════════════════════════════════════════════════════

def calculate_risk_score(text):
    """
    Computes a risk score ∈ [0, 1] using weighted keyword matching.
    Applies a sigmoid-like curve to avoid harsh jumps.
    """
    text_lower = text.lower()
    raw_score = 0.0
    matched_keywords = []

    for keyword, weight in DISTRESS_LEXICON.items():
        if keyword in text_lower:
            raw_score += weight
            matched_keywords.append((keyword, weight))

    # Subtract positive signals
    positive_reduction = 0.0
    for keyword, weight in POSITIVE_LEXICON.items():
        if keyword in text_lower:
            positive_reduction += weight

    raw_score = max(0.0, raw_score - positive_reduction)

    # Sigmoid normalization: maps raw_score to [0, 1] smoothly
    # At raw_score=0.5, output ≈ 0.5; at raw_score=1.5, output ≈ 0.9
    normalized = 1.0 / (1.0 + math.exp(-4.0 * (raw_score - 0.5)))

    logger.info(f"Risk Calc: matched={matched_keywords}, raw={raw_score:.2f}, positive_reduction={positive_reduction:.2f}, final={normalized:.3f}")
    return round(normalized, 3)


def calculate_confidence_score(text, emotion_data):
    """
    Measures alignment between text sentiment and facial expression.
    High alignment → high confidence; conflict → low confidence.
    Returns ∈ [0, 1].
    """
    if not emotion_data:
        return 0.5  # Neutral — no face data available

    detected_emotion = emotion_data.get('emotion', '').lower()
    face_confidence = emotion_data.get('score', 0.5)
    text_lower = text.lower()

    # Compute text sentiment polarity
    text_negative = sum(w for k, w in DISTRESS_LEXICON.items() if k in text_lower)
    text_positive = sum(w for k, w in POSITIVE_LEXICON.items() if k in text_lower)

    text_polarity = "positive" if text_positive > text_negative else ("negative" if text_negative > 0.1 else "neutral")

    # Face polarity
    positive_faces = {"happy", "surprised"}
    negative_faces = {"sad", "angry", "fearful", "disgusted"}
    face_polarity = "positive" if detected_emotion in positive_faces else ("negative" if detected_emotion in negative_faces else "neutral")

    # Alignment scoring
    if text_polarity == face_polarity:
        base_confidence = 0.85 + (face_confidence * 0.15)  # Strong alignment
    elif text_polarity == "neutral" or face_polarity == "neutral":
        base_confidence = 0.6  # Partial info
    else:
        base_confidence = 0.25  # Conflict detected (e.g., says "happy" but face angry)

    logger.info(f"Confidence Calc: text_polarity={text_polarity}, face_polarity={face_polarity}, face_conf={face_confidence:.2f}, result={base_confidence:.2f}")
    return round(base_confidence, 3)


def classify_state(text, emotion_data, risk_score):
    """
    Rule-based state classification using priority-ordered rules.
    Considers text keywords, facial expression, and risk score.
    """
    text_lower = text.lower()
    detected_emotion = emotion_data.get('emotion', 'neutral').lower() if emotion_data else 'neutral'

    for rule in STATE_RULES:
        # Check if risk threshold is met
        if risk_score < rule["min_risk"]:
            continue

        # Check for text signal match
        text_match = any(signal in text_lower for signal in rule["text_signals"])

        # Check for face signal match
        face_match = detected_emotion in rule["face_signals"] if rule["face_signals"] else False

        # Trigger: text match OR (face match with no text signals required)
        if text_match or (face_match and not rule["text_signals"]):
            return rule["state"]

    return "General Reflection"


def analyze_state_trends(current_state, history):
    """
    Detects persistent patterns across recent sessions.
    Returns (refined_state, is_trend_detected).
    """
    if not history or len(history) < 2:
        return current_state, False

    past_states = [h.get('state', '') for h in history[-5:]]

    trend_map = {
        "Anxiety / Panic": ("Persistent Anxiety Pattern", 2),
        "Fatigue / Burnout": ("Chronic Fatigue Pattern", 2),
        "Overthinking / Rumination": ("Recursive Thought Loop", 2),
        "Frustration / Anger": ("Escalating Frustration", 2),
    }

    if current_state in trend_map:
        trend_name, threshold = trend_map[current_state]
        if past_states.count(current_state) >= threshold:
            logger.info(f"Trend Detected: {trend_name} (seen {past_states.count(current_state)}x in last {len(past_states)} sessions)")
            return trend_name, True

    return current_state, False


def select_technique(state):
    """Maps current state to a therapeutic micro-technique."""
    return TECHNIQUE_MAP.get(state, "Empathetic Validation")


# ═════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═════════════════════════════════════════════════════════════

def get_behavioral_analysis(text, emotion_data, history=None):
    """
    Main scoring pipeline — fully heuristic, no LLM involvement.
    Returns a complete analysis dict for the frontend trace.
    """
    if emotion_data is None:
        emotion_data = {}
    if history is None:
        history = []

    # Step 1: Risk Scoring (weighted keyword + sigmoid)
    risk = calculate_risk_score(text)

    # Step 2: Confidence Scoring (text vs face alignment)
    confidence = calculate_confidence_score(text, emotion_data)

    # Step 3: State Classification (rule-based priority matching)
    base_state = classify_state(text, emotion_data, risk)

    # Step 4: Trend Analysis (session history pattern detection)
    state, is_trend = analyze_state_trends(base_state, history)

    # Step 5: Technique Selection (state → intervention mapping)
    technique = select_technique(state)

    # Build signal summary for frontend trace
    detected_emotion = emotion_data.get('emotion', 'none') if emotion_data else 'none'
    face_score = emotion_data.get('score', 0.0) if emotion_data else 0.0

    analysis = {
        "risk_score": risk,
        "confidence_score": confidence,
        "state": state,
        "selected_technique": technique,
        "is_trend": is_trend,
        # Extra fields for rich frontend trace
        "input_signals": {
            "face_emotion": detected_emotion,
            "face_confidence": round(face_score, 2),
            "text_length": len(text),
            "session_depth": len(history),
        },
        "engine_version": "2.0-heuristic",
    }

    logger.info(f"Analysis Complete: state={state}, risk={risk}, confidence={confidence}, technique={technique}, trend={is_trend}")
    return analysis
