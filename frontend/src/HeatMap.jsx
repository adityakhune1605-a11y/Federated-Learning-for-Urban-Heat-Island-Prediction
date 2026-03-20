import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

function getColor(score) {
  if (score > 0.7) return "red";
  if (score > 0.4) return "orange";
  return "green";
}

export default function HeatMap({ zones }) {
  return (
    <MapContainer center={[20.59, 78.96]} zoom={5} style={{ height: "400px" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {zones.map((z) => (
        <CircleMarker
          key={z.id}
          center={[z.lat, z.lon]}
          radius={10}
          pathOptions={{ color: getColor(z.score) }}
        >
          <Popup>
            <b>{z.name}</b><br />
            Temp: {z.temp.toFixed(2)}°C<br />
            Score: {(z.score * 100).toFixed(0)}%
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}