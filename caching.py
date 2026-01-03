import streamlit as st
import time

st.title("Streamlit Caching")

@st.cache_data
def slow_square(x):
  time.sleep(2)
  return x*x

if st.button("Clear Cache"):
  st.cache_data.clear()
  st.warning("Cache Cleared!")
  
st.title("Cache Example")
num = st.number_input("Enter a number",0,100)

with st.spinner("Computing"):
  result = slow_square(num)
st.success("Done!")
st.write("Result",result)
  
