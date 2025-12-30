import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

st.title("🌡️ Sensor Temperature Monitoring")

# Threshold
WARNING_TEMP = 70

# Initialize session state
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = pd.DataFrame(
        columns=["timestamp", "sensor", "temperature", "status"]
    )

# Sensors
sensors = ["Sensor A", "Sensor B", "Sensor C"]

st.subheader("Enter Temperature Readings")

# User inputs
inputs = {}
for sensor in sensors:
    inputs[sensor] = st.number_input(
        f"{sensor} Temperature (°C)",
        min_value=-50,
        max_value=150,
        value=25
    )

# Submit button
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
    st.success("Readings added!")

# Show table
st.subheader("Sensor Readings")
st.dataframe(st.session_state.sensor_data)

# Chart
if not st.session_state.sensor_data.empty:
    chart = alt.Chart(st.session_state.sensor_data).mark_line(point=True).encode(
        x="timestamp:T",
        y="temperature:Q",
        color="sensor:N",
        tooltip=["timestamp", "sensor", "temperature", "status"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# Alert section
st.subheader("🚨 Alerts")
alerts = st.session_state.sensor_data[
    st.session_state.sensor_data["temperature"] > WARNING_TEMP
]

if not alerts.empty:
    st.error("⚠️ High temperature detected!")
    st.dataframe(alerts)
else:
    st.success("All sensors are within safe limits ✅")
