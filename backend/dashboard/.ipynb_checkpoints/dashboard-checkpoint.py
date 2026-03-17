import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium import st_folium

st.set_page_config(page_title="Federated Learning - UHZ Dashboard", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Controls")
if st.sidebar.button("Start Training"):
    st.write("🚀 Training started on server... (simulated)")

# Global Model Accuracy
st.subheader("📊 Global Model Performance")
rounds = np.arange(1, 11)
accuracy = np.random.uniform(0.6, 0.9, 10)  # dummy data
fig, ax = plt.subplots()
ax.plot(rounds, accuracy, marker="o")
ax.set_xlabel("Round")
ax.set_ylabel("Accuracy")
st.pyplot(fig)

# Client Status
st.subheader("🖥️ Connected Clients")
clients = {"City A": "✅ Online", "City B": "✅ Online", "City C": "❌ Offline"}
st.table(clients.items())

# Urban Heat Zone Map
st.subheader("🌍 Urban Heat Zones Map")
m = folium.Map(location=[19.0760, 72.8777], zoom_start=5)
folium.CircleMarker([19.0760, 72.8777], radius=10, color="red", fill=True).add_to(m)
folium.CircleMarker([28.6139, 77.2090], radius=10, color="orange", fill=True).add_to(m)
st_folium(m, width=700, height=500)
