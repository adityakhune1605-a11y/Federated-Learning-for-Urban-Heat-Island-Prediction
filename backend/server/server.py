import flwr as fl

# Start a simple Federated Learning server
if __name__ == "__main__":
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=5),  # number of FL rounds
    )
