import streamlit as st
import pandas as pd

st.title("🔐 Real Login System (Basic)")

# Load users (real source)
users_df = pd.read_csv("data.csv")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# Login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")

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
