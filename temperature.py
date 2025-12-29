import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

st.title("🌡️ User Input Sensor Temperature Monitoring")

# Initialize session state for sensor readings
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = pd.DataFrame(columns=['timestamp', 'sensor', 'temperature', 'alert'])

# Define sensors
sensors = ['Sensor A', 'Sensor B', 'Sensor C']

st.subheader("Enter Temperature Readings")

# Create input fields for each sensor
user_inputs = {}
for sensor in sensors:
    user_inputs[sensor] = st.number_input(f"{sensor} Temperature (°C)", min_value=-50, max_value=150, value=25)

# Button to submit readings
if st.button("Submit Readings"):
    new_rows = []
    for sensor, temp in user_inputs.items():
        alert = temp > 70  # flag if temperature exceeds 70°C
        new_rows.append({'timestamp': datetime.now(), 'sensor': sensor, 'temperature': temp, 'alert': alert})
    
    st.session_state.sensor_data = pd.concat([st.session_state.sensor_data, pd.DataFrame(new_rows)], ignore_index=True)
    st.success("Readings submitted successfully!")

# Display table
st.subheader("Sensor Readings")
st.dataframe(st.session_state.sensor_data)

# Plot temperature readings
if not st.session_state.sensor_data.empty:
    chart = alt.Chart(st.session_state.sensor_data).mark_line(point=True).encode(
        x='timestamp:T',
        y='temperature:Q',
        color='sensor:N',
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
