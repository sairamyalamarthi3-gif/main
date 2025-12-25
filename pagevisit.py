import streamlit as st
import pandas as pd
from datetime import datetime

st.title("⏱️ Timestamped Page Visits")

# Initialize session state
if "visits" not in st.session_state:
    st.session_state.visits = []

# Simulate a page visit
if st.button("Simulate Page Visit"):
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.visits.append(visit_time)

# Convert to DataFrame for display
visits_df = pd.DataFrame(
    st.session_state.visits,
    columns=["Visit Time"]
)

# Show results
st.subheader("Visit History")
st.dataframe(visits_df)
