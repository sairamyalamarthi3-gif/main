import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

st.title("🌐 Real-Time Website Traffic Monitoring")

# Step 1: Simulate visitor counts
np.random.seed(42)
counts = np.random.randint(5, 20, size=30)

# Step 2: Generate timestamps matching the counts
timestamps = [datetime.now() - timedelta(minutes=i) for i in range(len(counts))]

# Step 3: Create dataframe
df = pd.DataFrame({
    "timestamp": timestamps[::-1],  # reverse to chronological order
    "visits": counts
})

# Step 4: Compute rolling average
df['moving_avg'] = df['visits'].rolling(window=5, min_periods=1).mean()

# Step 5: Detect spikes
threshold = 5
df['spike'] = df['visits'] > df['moving_avg'] + threshold

# Step 6: Display data
st.subheader("Traffic Data")
st.dataframe(df)

# Step 7: Plot chart with spikes highlighted
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
