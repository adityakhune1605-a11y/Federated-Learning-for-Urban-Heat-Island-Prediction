# client/client.py

import flwr as fl
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
def load_data():
    df = pd.read_csv("data/client1_data.csv")
    X = df[["temperature", "humidity"]].values
    y = df["label"].values
    return train_test_split(X, y, test_size=0.3, random_state=42)

X_train, X_test, y_train, y_test = load_data()
model = LogisticRegression()

# Define FL client
class HeatZoneClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        # Ensure model is initialized before sending parameters
        if not hasattr(model, "coef_"):
            model.fit(X_train, y_train)
        return [model.coef_, model.intercept_]

    def fit(self, parameters, config):
        model.coef_, model.intercept_ = parameters
        model.fit(X_train, y_train)
        return [model.coef_, model.intercept_], len(X_train), {}

    def evaluate(self, parameters, config):
        model.coef_, model.intercept_ = parameters
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        return float(acc), len(X_test), {"accuracy": acc}

# Start the client using updated API
if __name__ == "__main__":
    fl.client.start_client(
        server_address="127.0.0.1:8080",
        client=HeatZoneClient().to_client()
    )
