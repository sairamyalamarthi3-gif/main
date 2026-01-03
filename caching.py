import streamlit as st
import time

st.title("Streamlit Caching")

def heavy_calculation(n):
  time.sleep(5)
  return n*n

number = st.number_input("Enter a number",value = 5)
result = heavy_calculation(number)
st.write("Result",result)
  
