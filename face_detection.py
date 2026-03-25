import cv2
import base64
import numpy as np
from fer import FER
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use fast + stable detection globally
print("Loading FER detector...")
detector = FER(mtcnn=False)
buffer = []

@app.post("/detect")
async def detect(request: Request):
    global buffer
    try:
        data = await request.json()
        image_b64 = data.get("image")
        
        if not image_b64:
            return {"emotion": "Unknown"}
            
        # Parse base64
        header, encoded = image_b64.split(",", 1)
        image_data = base64.b64decode(encoded)
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"emotion": "Unknown"}

        # frame = cv2.resize(frame, (640, 480)) # Resize if needed, frontend sends small images usually

        results = detector.detect_emotions(frame)
        
        if results:
            # pick largest face (closest)
            largest_face = max(results, key=lambda x: x["box"][2] * x["box"][3])
            (x, y, w, h) = largest_face["box"]
            emotions = largest_face["emotions"]

            # reduce strict filtering 
            if w * h > 2000:
                emotion_name = max(emotions, key=emotions.get)
                confidence = emotions[emotion_name]
                
                # lower threshold so not always neutral
                if confidence > 0.2:
                    buffer.append(emotion_name)
                    if len(buffer) > 5:
                        buffer.pop(0)
                        
                    best_emotion = max(set(buffer), key=buffer.count)
                    return {"emotion": best_emotion}
                    
        return {"emotion": "Unknown"}

    except Exception as e:
        print("Error during emotion detection:", e)
        return {"emotion": "Unknown"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)