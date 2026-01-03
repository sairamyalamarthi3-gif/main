import streamlit as st
import pandas as pd
import time

st.title("Sales With Caching")

@st.cache_data
def calculate_data_sales():
  time.sleep(6)
  return 12500

st.write("Click the button to calculate total sales")

if st.button("Calculate Sales"):
  sales = calculate_data_sales
  st.success(f"Total sales today:£{sales}")
  
  
