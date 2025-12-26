import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Login-Based Inventory System")

# ---------------- USERS (Realistic demo users) ----------------
users = {
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

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# ---------------- INVENTORY DASHBOARD ----------------
if st.session_state.logged_in:
    st.subheader("📊 Inventory Dashboard")
    st.write(f"Logged in as: **{st.session_state.username}**")

    item = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=1, step=1)
    action = st.selectbox("Action", ["IN (Restock)", "OUT (Sale)"])

    if st.button("Update Inventory"):
        if item:
            record = {
                "Item": item,
                "Change": qty if action == "IN (Restock)" else -qty,
                "Action": action,
                "Updated By": st.session_state.username,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.inventory.append(record)
            st.success("Inventory updated!")
        else:
            st.error("Item name is required")

    # Inventory Table
    if st.session_state.inventory:
        df = pd.DataFrame(st.session_state.inventory)
        st.subheader("📋 Inventory Log")
        st.dataframe(df)

        # Stock Calculation
       if "Change" in df.columns:
         stock = df.groupby("Item")["Change"].sum()
         st.bar_chart(stock)
       else:
         st.error("Change column missing. Inventory data is invalid.")


    # Logout
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
