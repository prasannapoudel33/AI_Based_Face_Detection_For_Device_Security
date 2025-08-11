import face_recognition
import cv2
import pickle
import time
import subprocess
import pyttsx3
import os
import requests
from datetime import datetime

# === Send events to Node server ===
API_BASE = os.getenv("API_BASE", "http://localhost:8000")
INGEST_KEY = os.getenv("INGEST_KEY", "ingest-12345")

def send_event(user: str, event: str, confidence: float | None = None):
    try:
        payload = {
            "ts": datetime.utcnow().isoformat(),
            "user": user,
            "event": event,
            "confidence": confidence,
        }
        requests.post(
            f"{API_BASE}/api/events",
            json=payload,
            headers={"X-INGEST-KEY": INGEST_KEY},
            timeout=3,
        )
    except Exception as e:
        print("[EVENT SEND FAILED]", e)

# === Load trained model ===
with open("models/face_model.pkl", "rb") as f:
    model = pickle.load(f)

video = cv2.VideoCapture(0)
no_face_start = None
LOCK_DELAY = 10  # seconds

def speak_alert():
    engine = pyttsx3.init()
    engine.say("Unauthorized user detected. Locking the system.")
    engine.runAndWait()

print("[INFO] Monitoring started... Press 'q' to quit.")
last_label = None

while True:
    ret, frame = video.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    name = "Unknown"

    if face_encodings:
        try:
            name = model.predict([face_encodings[0]])[0]
        except Exception:
            name = "Unknown"

        if name == "prasanna":
            if last_label != "prasanna":
                send_event("prasanna", "recognized", confidence=0.99)
            no_face_start = None
        else:
            if no_face_start is None:
                no_face_start = time.time()
            if last_label != "random":
                send_event("random", "recognized", confidence=0.60)
    else:
        if no_face_start is None:
            no_face_start = time.time()

    # Lock if unauthorized for too long
    if no_face_start and time.time() - no_face_start > LOCK_DELAY:
        print("[SECURITY] Locking system due to unknown user...")
        speak_alert()
        send_event("random", "screen_off")
        subprocess.call(["cmd", "/c", "src\\win.bat"])
        break

    # Draw and display
    for (top, right, bottom, left) in face_locations:
        top, right, bottom, left = top*4, right*4, bottom*4, left*4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Face Monitoring", frame)
    last_label = "prasanna" if name == "prasanna" else "random"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
