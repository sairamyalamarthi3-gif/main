import streamlit as st
import time

st.title("Streamlit Caching")

@st.cache_data
def slow_square(x):
  time.sleep(2)
  return x*x

@st.cache_data
def slow_double(x:int):
  time.sleep(2)
  return x * 2

if st.button("Clear Cache"):
  st.cache_data.clear()
  st.warning("Cache Cleared!")
  
st.title("Cache Example")
num = st.number_input("Enter a number",0,100)

with st.spinner("Computing"):
  Squared = slow_square(num)

with st.spinner("Computing........"):
  Doubled = slow_double(num)
st.success("Done!")
st.write("Sqaure",Squared)
st.write("Double",Doubled)

  
