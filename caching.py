import streamlit as st
import pandas as pd
import time

st.title("With Caching")

@st.catche_data
def load_data():
  time.sleep(5)
  return pd.DataFrame({
    "item":["Apple","Banana","Orange"],
    "price":["5","10","8"]
  })

st.write("Data Loading")
data = load_data()
st.dataframe(data)
