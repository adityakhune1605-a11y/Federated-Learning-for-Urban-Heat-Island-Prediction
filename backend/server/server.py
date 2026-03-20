import flwr as fl

def main():
    print("Starting Federated Learning Server...")

    # Configure server
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,          # use all clients
        fraction_evaluate=1.0,
        min_fit_clients=2,         # minimum clients required
        min_evaluate_clients=2,
        min_available_clients=2,
    )

    # Start server
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=5),
        strategy=strategy,
    )

if __name__ == "__main__":
    main()