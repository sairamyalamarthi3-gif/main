import streamlit as st
st.title("Login Page")
username = st.text_input("User Name")
password = st.text_input("Password",type =  "password")
if st.button("Login"):
  if username == "admin" and password == "admin123":
    st.success("Login Successful")
  else:
    st.error("Incorrect Password")
##Show Dashboard if logged in
if logged_in:
  st.header("Dashboard")
  st.write("Welcome to the Login Page")
  
    
