# 📋🛡️ Face recognition -based Artificial Intelligence monitoring system for securing unattended device in work place to maintain data security

A lightweight system that continuously authenticates the active user via **face recognition** and **locks the screen** if an unknown user is present for 10s. Events are logged to **MongoDB** and visualized on a **React dashboard**.

## 🧩 What’s inside

* **Python monitor** (`monitor_embeddings.py`) – OpenCV + `face_recognition`, voice alert, screen-off.
* **Node/Express backend** (`server/`) – Stores events in MongoDB, JWT login, WebSocket updates.
* **React dashboard** (`monitor-dashboard-react/`) – Login, KPIs, charts, Monitoring (Start/Stop), Activity Log with presence %.

## 🔧 Tech

Python, OpenCV, face\_recognition, Node.js (Express + ws), MongoDB, React (Vite), Chart.js, JWT.

## 📂 Structure

```
AI_Based_Face_Detection_For_Device_Security/
├─ monitor_embeddings.py
├─ models/face_model.pkl
├─ src/win.bat
├─ server/               # backend API
│  ├─ .env
│  └─ src/index.js
└─ monitor-dashboard-react/   # frontend
   ├─ .env
   └─ src/...
```

## ⚙️ Environment

**server/.env**

```
MONGO_URI=mongodb://127.0.0.1:27017
DB_NAME=face_security
FIXED_USERNAME=admin
FIXED_PASSWORD=letmein123!
JWT_SECRET=<long_random_string>
JWT_ALG=HS256
INGEST_KEY=ingest-12345
PORT=8000
# (optional) PYTHON_EXE=py
```

**monitor-dashboard-react/.env**

```
VITE_API_BASE=http://localhost:8000
```

## 🚀 Run

1. **Start MongoDB** (service or `docker run -p 27017:27017 mongo`).
2. **Backend**

   ```bash
   cd server
   npm install
   npm run dev
   ```
3. **Frontend**

   ```bash
   cd ../monitor-dashboard-react
   npm install
   npm run dev
   ```
4. Open the app → **Login**: `admin / letmein123!`
   Go to **Monitoring → Start Monitoring** (spawns `monitor_embeddings.py`).

## 🔒 Behavior

* `prasanna` recognized → logged.
* Unknown/none > 10s → voice alert + `src/win.bat` (screen off).
* All events stored to MongoDB and shown live on the dashboard.
