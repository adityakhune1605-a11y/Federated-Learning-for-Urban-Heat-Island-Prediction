
# 🌆 Smart City UHZ Prediction using Federated Learning

## 📌 About the Project

This project focuses on predicting **Urban Heat Zones (UHZ)** using **Federated Learning (FL)**.

Instead of collecting all data in one place, each region (client) trains its own model locally and shares only the learned updates with a central server. This helps in maintaining **data privacy** while still building a strong global model.

The results are visualized on a **live dashboard**, where we can see which areas are hotter and need attention.

---

## 🧠 How the System Works

- Each **client** (city/region) trains a local model  
- A **server** aggregates all updates  
- A **Flask API (hosted on Render)** stores results  
- A **React dashboard** displays heat zones on a map  

In simple terms:
Clients → Server → Cloud API → Dashboard


---

## 🛠️ Technologies Used

- Python (Core logic)
- TensorFlow (Model training)
- Flower (Federated Learning framework)
- Flask (Backend API)
- React + Leaflet (Frontend dashboard)
- Render (Cloud deployment)

---

## ⚙️ How to Run the Project

Follow these steps carefully:

---

### 🔹 Step 1 — Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd FL-UHZ


---

### 🔹 Step 2 — Setup Python environment

⚠️ Use Python **3.8 or 3.10** (TensorFlow requirement)
cd backend/client
py -3.8 -m venv FLenv
FLenv\Scripts\activate


---

### 🔹 Step 3 — Install dependencies
pip install tensorflow==2.13.0
pip install flwr numpy scikit-learn requests


---

### 🔹 Step 4 — Start the FL server

Open a new terminal:
cd backend/server
python server.py


---

### 🔹 Step 5 — Run clients (in multiple terminals)
cd backend/client
python client.py 1
python client.py 2
python client.py 3


Each client simulates a different city.

---

### 🔹 Step 6 — Run frontend dashboard
cd frontend
npm install
npm run dev


---

### 🌐 Open in browser
http://localhost:5173


You should now see a map with heat zones updating in real-time.

---

## 📊 What You’ll See

- Colored regions on the map:
  - 🔴 Red → High heat zone  
  - 🟠 Orange → Moderate  
  - 🟢 Green → Low heat  

- Client performance (accuracy)  
- Continuous updates as training happens  

---

## 🧪 Current Implementation

Right now, the project uses **synthetic (random) data** to simulate real-world conditions like:
- Temperature  
- Humidity  
- Green cover  
- Population density  

This is done to demonstrate the working of the system.

---

## 🔥 Using Real Dataset in Future

When you get real data, follow this:

---

### 📥 Step 1 — Add dataset

Place your file here:
backend/data/uhz_data.csv


---

### 📄 Expected format

| temp | humidity | green_cover | population_density | label |
|------|----------|-------------|--------------------|-------|

---

### 🔧 Step 2 — Modify client code

Replace synthetic data in `client.py`:

#### ❌ Current:
```python
X = np.random.rand(500, 4)
✅ New:
import pandas as pd

df = pd.read_csv("../data/uhz_data.csv")

X = df[["temp", "humidity", "green_cover", "population_density"]].values
y = df["label"].values
📍 Step 3 — Add location data (optional)
If your dataset has coordinates:

lat = df["latitude"]
lon = df["longitude"]
Use them instead of random offsets.

🧠 Step 4 — Improve prediction logic
Instead of random temperature:

temp = base_temp + noise
Use actual data:

temp = np.mean(X[:, 0])
🚀 Future Improvements
Use real satellite data (NASA / MOSDAC)

Add IoT sensor inputs

Improve model architecture

Add time-based predictions

Deploy frontend online

👨‍💻 Team
Aditya Khune

Sharvari Kudia

Raviraj Dahiphale

Yadnyavalk Deshmukh

Guide: Prof. Geeta Kodabagi

🧠 What We Learned
Federated Learning concepts

Distributed model training

Cloud integration

Real-time visualization

⚠️ Notes
Do NOT upload virtual environments (FLenv/)

Use correct Python version for TensorFlow

First API request on Render may take time (cold start)

⭐ Final Note
This project demonstrates how cities can collaboratively tackle urban heat problems while preserving data privacy — a key requirement for future smart cities.
