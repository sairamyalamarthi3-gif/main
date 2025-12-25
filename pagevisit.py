import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📊 Visits Per Minute Dashboard")

# Initialize session state
if "visits" not in st.session_state:
    st.session_state.visits = []

# Simulate a page visit
if st.button("Simulate Page Visit"):
    visit_time = datetime.now()
    st.session_state.visits.append(visit_time)

# Convert visits to DataFrame
if st.session_state.visits:
    df = pd.DataFrame(st.session_state.visits, columns=["visit_time"])

    # Convert timestamp to minute-level
    df["minute"] = df["visit_time"].dt.strftime("%Y-%m-%d %H:%M")

    # Count visits per minute
    visits_per_minute = df["minute"].value_counts().sort_index()

    st.subheader("Visits Per Minute")
    st.bar_chart(visits_per_minute)

    st.subheader("Raw Visit Logs")
    st.dataframe(df)
else:
    st.info("No visits yet. Click the button to simulate visits.")

