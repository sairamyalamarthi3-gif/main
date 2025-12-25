import streamlit as st
import pandas as pd
from datetime import datetime
st.title("Real time Login System")
users = pd.read_csv("Book(Sheet1).csv")

## Initialize session state
if "logged_in" not in st.session_state:
  st.session_state_logged_in = False
if "username" not in st_session_state:
  st.session_state_username =""
if "role" not in st_session_state:
  st.session_state_role = ""

## Login Form

Username = st.text_input("Username")
Password = st.text_input("Password", type = "password")

if st.button("Login"):
  user = users_df[
         (users_df["username"] == username) &
         (users_df["password"] == password)
  ]

if not user.empty:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = user.iloc[0]["role"]
        st.success("Login successful!")
    else:
        st.error("Invalid credentials")
if st.session_state.logged_in:
    st.header("Dashboard")
    st.write(f"Welcome, {st.session_state.username}")
    st.write(f"Role: {st.session_state.role}")

  
