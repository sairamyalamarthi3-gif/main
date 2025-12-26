import streamlit as st
import pandas as pd

##Buttons
primary button = st.button("Primary", type = "primary")
secondary button = st.button("Secondary", type = "secondary")

if primary button:
   st.write("Hello from primary")
if secondary button:
   st.write("Hello from Secondary")
