# train_model.py

import os
import cv2
import pickle
import face_recognition
from sklearn import neighbors
from sklearn.model_selection import train_test_split

# CONFIG
DATASET_DIR = 'dataset/prasanna'
MODEL_PATH = 'models/face_recognition_model.pkl'
ENCODINGS = []
NAMES = []

def encode_faces():
    print("[INFO] Loading images from dataset...")
    image_files = [f for f in os.listdir(DATASET_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for img_file in image_files:
        path = os.path.join(DATASET_DIR, img_file)
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        if len(encodings) == 1:
            ENCODINGS.append(encodings[0])
            NAMES.append("your_name")
        else:
            print(f"[WARNING] Skipping {img_file}: found {len(encodings)} faces")

    print(f"[INFO] Encoded {len(ENCODINGS)} images.")

def train_knn():
    print("[INFO] Training KNN classifier...")
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', weights='distance')
    knn_clf.fit(ENCODINGS, NAMES)
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(knn_clf, f)

    print(f"[INFO] Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    encode_faces()
    if ENCODINGS:
        train_knn()
    else:
        print("[ERROR] No valid face encodings found.")
