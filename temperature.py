import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt

st.title("🌡️ Real-Time Sensor Temperature Monitoring")

# Initialize session state for sensor readings
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = pd.DataFrame(columns=['timestamp', 'sensor', 'temperature', 'alert'])

# Simulate sensors
sensors = ['Sensor A', 'Sensor B', 'Sensor C']

# Button to simulate new readings
if st.button("Add New Temperature Readings"):
    new_rows = []
    for sensor in sensors:
        temp = np.random.randint(20, 100)  # temperature in Celsius
        alert = temp > 70  # flag if temperature exceeds 70°C
        new_rows.append({'timestamp': datetime.now(), 'sensor': sensor, 'temperature': temp, 'alert': alert})
    st.session_state.sensor_data = pd.concat([st.session_state.sensor_data, pd.DataFrame(new_rows)], ignore_index=True)

# Display table
st.subheader("Sensor Readings")
st.dataframe(st.session_state.sensor_data)

# Plot temperature readings
chart = alt.Chart(st.session_state.sensor_data).mark_line(point=True).encode(
    x='timestamp:T',
    y='temperature:Q',
    color=alt.Color('sensor:N'),
    tooltip=['timestamp', 'sensor', 'temperature', 'alert']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Show alerts
st.subheader("Alerts")
alerts = st.session_state.sensor_data[st.session_state.sensor_data['alert'] == True]
if not alerts.empty:
    st.write(alerts)
else:
    st.write("No alerts! All sensors are within safe temperature range.")
