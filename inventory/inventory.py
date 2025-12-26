import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Inventory System", layout="centered")
st.title("📦 Login-Based Inventory System")

# ---------------- DEMO USERS ----------------
USERS = {
    "admin": "admin123",
    "staff": "staff123"
}

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------------- INV
