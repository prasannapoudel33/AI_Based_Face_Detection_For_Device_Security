import cv2
import mediapipe as mp
import numpy as np
import pickle
import time
import subprocess
import os

# === CONFIGURATION ===
MODEL_PATH = "face_model.pkl"
LOCK_SCRIPT = "src/win.bat"
AUTHORIZED_USER = "prasanna"
CONFIDENCE_THRESHOLD = 0.85  # Try 0.9 if still false positives
LOCK_DELAY = 10  # seconds

# === Load trained model ===
if not os.path.exists(MODEL_PATH):
    print(f"[ERROR] Model file not found: {MODEL_PATH}")
    exit()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# === Init MediaPipe face detector ===
mp_face = mp.solutions.face_detection
detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

def extract_face_embedding(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = detector.process(rgb)
    if result.detections:
        for detection in result.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = rgb.shape
            x1, y1 = int(bbox.xmin * w), int(bbox.ymin * h)
            x2, y2 = x1 + int(bbox.width * w), y1 + int(bbox.height * h)
            face_img = rgb[max(0, y1):y2, max(0, x1):x2]
            try:
                face_resized = cv2.resize(face_img, (100, 100))
                return face_resized.flatten() / 255.0
            except:
                return None
    return None

# === Initialize Webcam and Monitoring ===
cap = cv2.VideoCapture(0)
no_face_start = None

print("[INFO] Monitoring started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    embedding = extract_face_embedding(frame)
    name = "random"
    confidence = 0.0

    if embedding is not None:
        proba = model.predict_proba([embedding])[0]
        confidence = np.max(proba)
        prediction = model.classes_[np.argmax(proba)]

        # Show prediction and confidence in console
        print(f"[DEBUG] Predicted: {prediction}, Confidence: {confidence:.2f}")

        # Only accept prasanna if confidence is high
        if prediction == AUTHORIZED_USER and confidence >= CONFIDENCE_THRESHOLD:
            name = AUTHORIZED_USER
            no_face_start = None
        else:
            name = "random"
            if no_face_start is None:
                no_face_start = time.time()
    else:
        name = "No face"
        if no_face_start is None:
            no_face_start = time.time()

    # Lock the device if no authorized face detected for threshold duration
    if no_face_start and (time.time() - no_face_start > LOCK_DELAY):
        print("[SECURITY] No authorized face detected! Locking device...")
        if os.path.exists(LOCK_SCRIPT):
            subprocess.call([LOCK_SCRIPT])
        else:
            print(f"[ERROR] Lock script not found at: {LOCK_SCRIPT}")
        break

    # Draw result on screen
    label = f"{name} ({confidence:.2f})" if name != "No face" else "No face detected"
    color = (0, 255, 0) if name == AUTHORIZED_USER else (0, 0, 255)
    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



