import streamlit as st
import pandas as pd
st.title("Real Time Page Monitoring System")

## Initialize Session State
if "page_visits" not in st.session_state:
  st.session_state.page_visits = 0

##Simulate a page visit
if st.button("Simulate Page Visit"):
  st.session_state.page_visits += 1 

## Display Real time metric
st.metric(
  label = "Total Page Visits",
  value = st.session_state.page_visits
)

st.write("Current Visit Count:" , st.session_state.page_visits)
