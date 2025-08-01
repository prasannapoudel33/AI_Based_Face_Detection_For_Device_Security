# -*- coding: utf-8 -*-
"""Face_recognition_cybersecurity_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12ZHMd-3wGPjCLDzePRHno_OX3lQRcIK_

# NEW TEST CODE
"""

!pip install mediapipe opencv-python scikit-learn numpy

import os
import cv2
import mediapipe as mp
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Dataset paths
DATA_DIR = "/content/drive/MyDrive/Colab Notebooks/dataset"
CLASSES = ["prasanna", "random"]

# Face detection setup
mp_face = mp.solutions.face_detection

def extract_face_embedding(image):
    with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as detector:
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
                    resized = cv2.resize(face_img, (100, 100))
                    return resized.flatten() / 255.0
                except:
                    return None
        return None

# Prepare training data
X, y = [], []
for label in CLASSES:
    folder = os.path.join(DATA_DIR, label)
    for img_file in os.listdir(folder):
        if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, img_file)
            img = cv2.imread(path)
            emb = extract_face_embedding(img)
            if emb is not None:
                X.append(emb)
                y.append(label)
            else:
                print(f"[WARN] No face in: {img_file}")

# Train KNN model
print("[INFO] Training KNN...")
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

# Save model
with open("face_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("[INFO] Model trained and saved as face_model.pkl")

from google.colab import files
files.download("face_model.pkl")

