import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

st.title("🌐 Real-Time Website Traffic Monitoring")

# Simulate visitor timestamps
np.random.seed(42)
timestamps = [datetime.now() - timedelta(minutes=i) for i in range(30)]
counts = np.random.randint(5, 30, size=20)

df = pd.DataFrame({"timestamp": timestamps[::-1], "visits": counts})

# Compute rolling average
df['moving_avg'] = df['visits'].rolling(window=5, min_periods=1).mean()

# Detect spikes: if current visits > moving_avg + threshold
threshold = 5
df['spike'] = df['visits'] > df['moving_avg'] + threshold

st.subheader("Traffic Data")
st.dataframe(df)

# Plot visitors per minute with spikes highlighted
chart = alt.Chart(df).mark_line(point=True).encode(
    x='timestamp:T',
    y='visits:Q',
    color=alt.condition(
        alt.datum.spike == True,
        alt.value('red'),
        alt.value('blue')
    ),
    tooltip=['timestamp', 'visits', 'moving_avg', 'spike']
).interactive()

st.altair_chart(chart, use_container_width=True)
