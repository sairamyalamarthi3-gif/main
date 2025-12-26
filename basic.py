import streamlit as st
import pandas as pd

##Buttons
primary_button = st.button("Primary", type = "primary")
secondary_button = st.button("Secondary", type = "secondary")

if primary_button:
   st.write("Hello from primary")
if secondary_button:
   st.write("Hello from Secondary")
st.divider()
## checkbox
checkbox = st.checkbox("Remember me")
if checkbox:
   st.write("I will remember you")
else:
   st.write("I will not remember you")

st.divider()
##Radio Buttons
df = pd.read_csv("data.csv")
radio = st.radio("Choose a column",options = df.columns[1:], index = 1, horizontal = False)
st.write(radio)

st.divider()
##Select box
select= st.selectbox("Choose a column", options = df.columns[1:].index = 1, vertical = True)
st.write(select)
st.divider()
