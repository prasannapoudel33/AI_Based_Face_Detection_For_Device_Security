# AI-Based Behavioral Detection System for Device Security

This project implements a workplace device security system that uses real-time face detection and recognition to ensure only the authorized user can access the system. If the authorized user's face is not detected for a specified time, the device automatically locks itself.

---

## 🎯 Objective

To improve workplace device security by:
- Detecting the authorized user's presence using a webcam
- Locking the device if the user leaves the frame for more than 10 seconds

---

## 🧠 Core Features

- **Real-time face detection** using OpenCV
- **Face recognition** using a custom-trained model on the authorized user's images
- **Timed auto-lock**: Locks device if face is not detected for 10 seconds
- **Cross-platform flexibility** (Windows-based locking)

---

## 🗂️ Project Structure

Cyber_Security_Project/
├── dataset/
│ └── yourname/ # Folder of your face images
├── models/
│ └── face_recognition_model.pkl
├── src/
│ ├── train_model.py # Train face recognition model
│ ├── detect_and_lock.py # Real-time detection + lock
│ ├── lock_device.bat # Triggers Windows lock
│ └── utils.py # Helper functions
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

1. **Install dependencies** (preferably inside a virtual environment):

```bash
pip install -r requirements.txt

Add your face images to:
dataset/yourname/

Train the model:
python src/train_model.py

Run the detection system:
python src/detect_and_lock.py

🔐 Security Mechanism
The system continuously monitors the webcam

If no recognized face is detected for 10 seconds:

The .bat file is triggered to lock the workstation

