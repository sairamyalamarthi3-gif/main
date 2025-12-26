import streamlit as st
import pandas as pd

##Buttons
primary_button = st.button("Primary", type = "primary")
secondary_button = st.button("Secondary", type = "secondary")

if primary_button:
   st.write("Hello from primary")
if secondary_button:
   st.write("Hello from Secondary")
