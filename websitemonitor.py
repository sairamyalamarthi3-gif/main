import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt
import time

st.title("🌐 Real-Time Website Traffic Monitoring")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['timestamp', 'visits', 'moving_avg', 'spike'])

# Button to simulate new visitor data
if st.button("Add New Visitor Count"):
    new_count = np.random.randint(5, 20)
    new_timestamp = datetime.now()
    
    # Append new row
    new_row = pd.DataFrame({
        'timestamp': [new_timestamp],
        'visits': [new_count]
    })
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    
    # Recalculate rolling average and spike detection
    st.session_state.df['moving_avg'] = st.session_state.df['visits'].rolling(window=5, min_periods=1).mean()
    st.session_state.df['spike'] = st.session_state.df['visits'] > st.session_state.df['moving_avg'] + 5

# Display dataframe
st.subheader("Traffic Data")
st.dataframe(st.session_state.df)

# Plot chart
chart = alt.Chart(st.session_state.df).mark_line(point=True).encode(
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
