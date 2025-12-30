import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
import time

# -----------------------
# CONFIG
# -----------------------
WARNING_TEMP = 70
REFRESH_SECONDS = 5

# -----------------------
# SESSION STATE SETUP
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = pd.DataFrame(
        columns=["timestamp", "sensor", "temperature", "status"]
    )

# -----------------------
# LOGIN PAGE
# -----------------------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Simple demo login (real apps use DB/auth)
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

    st.stop()  # Stop here if not logged in

# -----------------------
# DASHBOARD
# -----------------------
st.title("🌡️ Sensor Temperature Dashboard")
st.caption("Auto-refreshes every 5 seconds")

# Logout
if st.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

# -----------------------
# USER INPUT
# -----------------------
st.subheader("Enter Temperature Readings")

sensors = ["Sensor A", "Sensor B", "Sensor C"]
inputs = {}

for sensor in sensors:
    inputs[sensor] = st.number_input(
        f"{sensor} Temperature (°C)",
        min_value=-50,
        max_value=150,
        value=25,
        key=sensor
    )

if st.button("Submit Readings"):
    rows = []
    for sensor, temp in inputs.items():
        status = "⚠️ High Temperature" if temp > WARNING_TEMP else "✅ Normal"
        rows.append({
            "timestamp": datetime.now(),
            "sensor": sensor,
            "temperature": temp,
            "status": status
        })

    st.session_state.sensor_data = pd.concat(
        [st.session_state.sensor_data, pd.DataFrame(rows)],
        ignore_index=True
    )
    st.success("Readings saved")

# -----------------------
# DATA DISPLAY
# -----------------------
st.subheader("📊 Sensor Readings")
st.dataframe(st.session_state.sensor_data)

# -----------------------
# ALERTS
# -----------------------
alerts = st.session_state.sensor_data[
    st.session_state.sensor_data["temperature"] > WARNING_TEMP
]

st.subheader("🚨 Alerts")
if not alerts.empty:
    st.error("⚠️ High temperature detected!")
    st.dataframe(alerts)
else:
    st.success("All sensors are within safe limits ✅")

# -----------------------
# CHART
# -----------------------
if not st.session_state.sensor_data.empty:
    chart = alt.Chart(st.session_state.sensor_data).mark_line(point=True).encode(
        x="timestamp:T",
        y="temperature:Q",
        color="sensor:N",
        tooltip=["timestamp", "sensor", "temperature", "status"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# -----------------------
# AUTO REFRESH
# -----------------------
time.sleep(REFRESH_SECONDS)
st.experimental_rerun()
