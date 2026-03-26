import logging

logger = logging.getLogger("MindfulAI-Scoring")

# 1. Distress Keywords for Risk Scoring
DISTRESS_KEYWORDS = {
    "high": ["suicide", "kill myself", "end it", "no reason to live", "hurt myself"],
    "medium": ["hopeless", "cannot go on", "tired of everything", "alone", "help", "pain"],
    "low": ["sad", "upset", "unhappy", "stressed", "worried"]
}

def calculate_risk_score(text):
    """
    Computes a risk score between 0 and 1 based on distress keywords.
    """
    text = text.lower()
    score = 0.0
    
    for word in DISTRESS_KEYWORDS["high"]:
        if word in text: score += 0.8
    for word in DISTRESS_KEYWORDS["medium"]:
        if word in text: score += 0.4
    for word in DISTRESS_KEYWORDS["low"]:
        if word in text: score += 0.1
        
    return min(score, 1.0)

def calculate_confidence_score(text, emotion_data):
    """
    Evaluates pattern consistency between Text Sentiment and Face Emotion.
    Returns 0 to 1.
    """
    if not emotion_data:
        return 0.5  # Neutral confidence if no face data
    
    detected_emotion = emotion_data.get('emotion', '').lower()
    text = text.lower()
    
    # Simple semantic match
    is_positive_text = any(word in text for word in ["happy", "good", "great", "better", "okay"])
    is_negative_text = any(word in text for word in ["sad", "bad", "terrible", "worst", "anxious", "scared"])
    
    is_positive_face = detected_emotion in ["happy", "surprised"]
    is_negative_face = detected_emotion in ["sad", "angry", "fearful", "disgusted"]
    
    # Conflict Detection logic
    if (is_positive_text and is_negative_face) or (is_negative_text and is_positive_face):
        return 0.3  # Low confidence due to conflict
    
    if (is_positive_text and is_positive_face) or (is_negative_text and is_negative_face):
        return 0.9  # High confidence due to alignment
        
    return 0.7  # Default moderate confidence

def classify_state(text, emotion_data):
    """
    Categorizes the user's mental state based on multimodal signals.
    """
    detected_emotion = emotion_data.get('emotion', 'neutral').lower()
    text = text.lower()
    
    if "end it" in text or "kill myself" in text or "suicide" in text:
        return "Immediate Crisis/High Risk"
    if "panic" in text or "scared" in text or detected_emotion == "fearful":
        return "Anxiety/Panic"
    if "tired" in text or "exhausted" in text or "burnout" in text:
        return "Fatigue/Burnout"
    if "thinking" in text and "always" in text:
        return "Overthinking"
    if detected_emotion == "sad" or "sad" in text:
        return "Low Mood/Sadness"
    if detected_emotion == "angry" or "frustrated" in text:
        return "Frustration"
        
    return "General Reflection"

def select_technique(state):
    """
    Maps mental states to specific therapeutic micro-techniques (Point 6 of Loop).
    """
    TECHNIQUE_MAP = {
        "Anxiety/Panic": "Breathing Exercise (4-7-8 Technique)",
        "Fatigue/Burnout": "Grounding (5-4-3-2-1 Technique)",
        "Overthinking": "CBT Reframing",
        "Low Mood/Sadness": "Behavioral Activation (Small wins)",
        "Frustration": "Physical Reset (Muscle relaxation)",
        "General Reflection": "Validating Reflection"
    }
    return TECHNIQUE_MAP.get(state, "Validating Reflection")

def analyze_state_trends(current_state, history):
    """
    Refines the state based on historical trends (Contextual Awareness).
    """
    if not history:
        return current_state, False
    
    # Extract last 3-5 states
    past_states = [h.get('state') for h in history if h.get('state')]
    
    # Pattern: Persistent Fatigue
    if current_state == "Fatigue/Burnout" and past_states.count("Fatigue/Burnout") >= 2:
        return "Chronic Fatigue Pattern", True
        
    # Pattern: Rising Anxiety
    if current_state == "Anxiety/Panic" and past_states.count("Anxiety/Panic") >= 2:
        return "Persistent Anxiety Pattern", True

    # Pattern: Stuck in Overthinking
    if current_state == "Overthinking" and past_states.count("Overthinking") >= 2:
        return "Recursive Thought Loop", True
        
    return current_state, False

def get_behavioral_analysis(text, emotion_data, history=None):
    """
    Main entry point for the scoring engine.
    """
    # Safety Check: Ensure emotion_data is at least an empty dict
    if emotion_data is None:
        emotion_data = {}
        
    if history is None:
        history = []
        
    risk = calculate_risk_score(text)
    confidence = calculate_confidence_score(text, emotion_data)
    
    # 1. Initial State Classification
    base_state = classify_state(text, emotion_data)
    
    # 2. Contextual Refinement (Phase 2: Step 9)
    state, is_trend = analyze_state_trends(base_state, history)
    
    # 3. Technique Selection (Adapts to trend)
    technique = select_technique(state)
    if is_trend:
        # Override technique for persistent patterns
        if "Anxiety" in state:
            technique = "Advanced Grounding + Clinical Referral Suggestion"
        elif "Fatigue" in state:
            technique = "Energy Conservation Strategy (Pacing)"
        elif "Overthinking" in state:
            technique = "Thought-Stopping Visualization"

    return {
        "risk_score": risk,
        "confidence_score": confidence,
        "state": state,
        "selected_technique": technique,
        "is_trend": is_trend
    }
