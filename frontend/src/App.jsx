import { useEffect, useState } from "react";
import api from "./api";
import HeatMap from "./HeatMap";

function App() {
  const [zones, setZones] = useState([]);
  const [clients, setClients] = useState([]);

  const fetchData = async () => {
    try {
      const z = await api.get("/heat_zones");
      const c = await api.get("/clients");

      setZones(z.data);
      setClients(c.data);
    } catch (err) {
      console.error("API error", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>🌆 Smart City UHZ Dashboard</h1>

      <h2>🔥 Heat Zones</h2>
      <HeatMap zones={zones} />

      <h2>👥 Clients</h2>
      <ul>
        {clients.map((c) => (
          <li key={c.id}>
            {c.name} — Accuracy: {c.last_accuracy?.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;