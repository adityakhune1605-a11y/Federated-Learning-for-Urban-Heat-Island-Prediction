import flwr as fl
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
import requests
import sys
import uuid
import time

# 🔥 YOUR RENDER URL
BRIDGE_URL = "https://federated-learning-for-urban-heat-island.onrender.com/api"

# -------------------------------
# DATA (Simulated Urban Data)
# -------------------------------
def load_data(seed):
    np.random.seed(seed)

    X = np.random.rand(500, 4)
    y = (X[:, 0] + X[:, 3] > 1).astype(int)

    return train_test_split(X, y, test_size=0.2, random_state=seed)

# -------------------------------
# MODEL
# -------------------------------
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(4,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model

# -------------------------------
# CLIENT CLASS
# -------------------------------
class UHZClient(fl.client.NumPyClient):

    def __init__(self, seed):
        self.id = f"client_{seed}_{uuid.uuid4().hex[:4]}"
        self.model = build_model()

        self.x_train, self.x_test, self.y_train, self.y_test = load_data(seed)

        # 🌍 City coordinates
        cities = [
            (18.5204, 73.8567),  # Pune
            (19.0760, 72.8777),  # Mumbai
            (28.7041, 77.1025),  # Delhi
        ]

        self.lat, self.lon = cities[seed % len(cities)]

        # Register client
        try:
            requests.post(
                f"{BRIDGE_URL}/update_client",
                json={
                    "id": self.id,
                    "name": self.id,
                    "samples": len(self.x_train),
                    "online": True
                },
                timeout=5
            )
        except:
            print("⚠️ Bridge connection failed")

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)

        # Train locally
        self.model.fit(
            self.x_train,
            self.y_train,
            epochs=2,
            batch_size=16,
            verbose=0
        )

        loss, acc = self.model.evaluate(self.x_test, self.y_test, verbose=0)

        # Send metrics
        try:
            requests.post(
                f"{BRIDGE_URL}/update_client",
                json={
                    "id": self.id,
                    "samples": len(self.x_train),
                    "last_accuracy": float(acc),
                    "last_loss": float(loss),
                    "online": True
                },
                timeout=5
            )
        except:
            print("⚠️ Failed to send metrics")

        # -------------------------------
        # HEAT ZONE GENERATION (IMPROVED)
        # -------------------------------
        try:
            zones = []

            # Real area names (better for demo)
            areas = ["Shivajinagar", "Kothrud", "Hadapsar", "Baner", "Viman Nagar"]

            # Base temperature from model (stable)
            base_temp = float(np.mean(self.x_train[:, 0]) * 40)

            for i in range(5):
                offset_lat = self.lat + (np.random.rand() - 0.5) * 0.02
                offset_lon = self.lon + (np.random.rand() - 0.5) * 0.02

                # Slight variation (realistic)
                temp = base_temp + np.random.uniform(-2, 2)
                score = float(min(1, max(0, temp / 45)))

                zones.append({
                    "id": f"{self.id}_{i}",
                    "name": areas[i],
                    "lat": offset_lat,
                    "lon": offset_lon,
                    "temp": temp,
                    "score": score
                })

            requests.post(
                f"{BRIDGE_URL}/update_zones",
                json={"zones": zones},
                timeout=5
            )

        except:
            print("⚠️ Failed to send zones")

        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, acc = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        return loss, len(self.x_test), {"accuracy": acc}

# -------------------------------
# RUN CLIENT (CONTINUOUS)
# -------------------------------
if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42

    while True:
        print("🔁 Client restarting...")

        client = UHZClient(seed)

        try:
            fl.client.start_client(
                server_address="127.0.0.1:8080",
                client=client.to_client(),
            )
        except Exception as e:
            print("⚠️ Connection failed, retrying...", e)

        time.sleep(5)