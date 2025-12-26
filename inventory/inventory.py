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

# ---------------- INVENTORY DASHBOARD ----------------
if st.session_state.logged_in:
    st.subheader("📊 Inventory Dashboard")
    st.write(f"Logged in as: **{st.session_state.username}**")

    # Inventory input
    item = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    action = st.selectbox("Action", ["IN (Restock)", "OUT (Sale)"])

    if st.button("Update Inventory"):
        if item:
            record = {
                "Item": item,
                "Change": quantity if action == "IN (Restock)" else -quantity,
                "Action": action,
                "Updated By": st.session_state.username,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.inventory.append(record)
            st.success("Inventory updated")
        else:
            st.error("Item name is required")

    # Show inventory data
    if st.session_state.inventory:
        df = pd.DataFrame(st.session_state.inventory)

        st.subheader("📋 Inventory Log")
        st.dataframe(df, use_container_width=True)

        # Stock calculation (FIXED)
        stock = df.groupby("Item")["Change"].sum()

        st.subheader("📦 Current Stock Levels")
        st.bar_chart(stock)

    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
