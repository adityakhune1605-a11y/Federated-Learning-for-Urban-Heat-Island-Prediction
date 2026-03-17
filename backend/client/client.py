import flwr as fl
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

# -------------------------------
# 1. Create synthetic UHZ dataset
# -------------------------------
def load_data(seed):
    np.random.seed(seed)
    # Features: [temp, humidity, green_cover, population_density]
    X = np.random.rand(500, 4)
    y = (X[:, 0] + X[:, 3] > 1).astype(int)  # Hotspot rule
    return train_test_split(X, y, test_size=0.2, random_state=seed)

# -------------------------------
# 2. Build model
# -------------------------------
def build_model(input_dim=4):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_dim,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

# -------------------------------
# 3. Federated Client
# -------------------------------
class UHZClient(fl.client.NumPyClient):
    def __init__(self, seed):
        self.model = build_model()
        self.x_train, self.x_test, self.y_train, self.y_test = load_data(seed)

    def get_parameters(self, config):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        self.model.fit(self.x_train, self.y_train, epochs=2, batch_size=16, verbose=0)
        return self.model.get_weights(), len(self.x_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, acc = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        return loss, len(self.x_test), {"accuracy": acc}

# -------------------------------
# 4. Run client
# -------------------------------
if __name__ == "__main__":
    import sys
    # Allow unique seeds per client (simulate diff regions)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    client = UHZClient(seed=seed)

    fl.client.start_client(
        server_address="127.0.0.1:8080",  # Replace with server IP if cloud
        client=client.to_client(),
    )
