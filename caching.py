import streamlit as st
import time

st.title("Streamlit Caching")

@st.cache_data
def slow_square(x):
  time.sleep(2)
  return x*x

st.title("Cache Example")
num = st.number_input("Enter a number",0,100)
result = slow_square(num)
st.write("Result",result)
  
