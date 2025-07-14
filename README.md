**AI-Based Behavioral Detection System for Device Security in Workplace**
Features:

* Face detection using webcam
* Face recognition based on your dataset
* 10-second timer if face is absent
* Locks device using `.bat` or WinAPI

---

## 🧱 Suggested File System Structure

```
behavioral-security/
├── dataset/                   # images for training
│   └── yourname/              # Folder of face images (used for labeling)
│       ├── img1.jpg
│       ├── img2.jpg
│       └── ...
├── models/
│   └── face_recognition_model.pkl  # Trained face embedding classifier
├── src/
│   ├── train_model.py         # Trains the face recognition model
│   ├── detect_and_lock.py     # Main script: detect face + trigger lock
│   ├── lock_device.bat        # Windows batch file to lock screen
│   └── utils.py               # Helper functions (encoding, loading, etc.)
├── requirements.txt           # List of required packages
└── README.md                  # Project overview and usage
```

---

## 🔍 File Descriptions

* **`train_model.py`**: Encodes your images, extracts embeddings (e.g., using `face_recognition`), and trains an SVM or KNN.
* **`detect_and_lock.py`**: Uses webcam to detect your face in real time. Starts 10-sec timer if you’re not seen → triggers lock.
* **`lock_device.bat`**: Simple script:

  ```bat
  rundll32.exe user32.dll,LockWorkStation
  ```
* **`face_recognition_model.pkl`**: Trained model saved with `pickle`.
* **`utils.py`**: Image-to-embedding functions, video capture logic, etc.

---

## ✅ Dependencies (`requirements.txt`)

```txt
face_recognition
opencv-python
imutils
numpy
scikit-learn
```

---
