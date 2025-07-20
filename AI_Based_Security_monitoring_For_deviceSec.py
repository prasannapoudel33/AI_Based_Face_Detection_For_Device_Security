import cv2
import mediapipe as mp
import numpy as np
import pickle
import time
import subprocess
from sklearn.neighbors import KNeighborsClassifier

# Load trained model
with open("models/face_model.pkl", "rb") as f:
    model = pickle.load(f)

# Init MediaPipe
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
            face_resized = cv2.resize(face_img, (100, 100))
            return face_resized.flatten() / 255.0
    return None

# Initialize webcam
cap = cv2.VideoCapture(0)

no_face_start = None
LOCK_DELAY = 10  # seconds

print("[INFO] Starting monitoring... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    embedding = extract_face_embedding(frame)
    name = "Unknown"

    if embedding is not None:
        prediction = model.predict([embedding])[0]
        name = prediction

        # If recognized user, reset timer
        if name == "prasanna":  # Change to your actual label
            no_face_start = None
        else:
            if no_face_start is None:
                no_face_start = time.time()
    else:
        if no_face_start is None:
            no_face_start = time.time()

    # Lock device after timeout
    if no_face_start and (time.time() - no_face_start > LOCK_DELAY):
        print("[SECURITY] No authorized face detected! Locking device...")
        subprocess.call(["src/lock.bat"])
        break

    cv2.putText(frame, f"User: {name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
