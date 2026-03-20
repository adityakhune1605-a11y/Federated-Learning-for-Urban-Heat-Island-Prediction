from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# 🔹 Store system data
STATE = {
    "clients": {},   # client info
    "zones": {},     # heat zones
    "metrics": []    # training history
}

LOCK = threading.Lock()

# -------------------------------
# GET APIs (Frontend uses these)
# -------------------------------

@app.route("/api/clients", methods=["GET"])
def get_clients():
    with LOCK:
        return jsonify(list(STATE["clients"].values()))

@app.route("/api/heat_zones", methods=["GET"])
def get_zones():
    with LOCK:
        return jsonify(list(STATE["zones"].values()))

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    with LOCK:
        return jsonify(STATE["metrics"])

# -------------------------------
# POST APIs (Clients send data)
# -------------------------------

@app.route("/api/update_client", methods=["POST"])
def update_client():
    data = request.json

    client_id = data["id"]

    with LOCK:
        STATE["clients"][client_id] = {
            "id": client_id,
            "name": data.get("name", client_id),
            "samples": data.get("samples", 0),
            "last_accuracy": data.get("last_accuracy"),
            "last_loss": data.get("last_loss"),
            "online": data.get("online", True),
            "updated_at": time.time()
        }

    return jsonify({"status": "client updated"})


@app.route("/api/update_zones", methods=["POST"])
def update_zones():
    data = request.json

    with LOCK:
        for z in data["zones"]:
            STATE["zones"][z["id"]] = {
                "id": z["id"],
                "name": z["name"],
                "lat": z["lat"],
                "lon": z["lon"],
                "temp": z["temp"],
                "score": z["score"],
                "updated_at": time.time()
            }

    return jsonify({"status": "zones updated"})


@app.route("/api/add_metric", methods=["POST"])
def add_metric():
    data = request.json

    with LOCK:
        STATE["metrics"].append({
            "round": data["round"],
            "accuracy": data["accuracy"],
            "loss": data["loss"],
            "timestamp": time.time()
        })

    return jsonify({"status": "metric added"})

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)