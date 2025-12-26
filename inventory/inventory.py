import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Inventory System (Stable Version)")

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "inventory" not in st.session_state:
    st.session_state.inventory = []

USERS = {
    "admin": "admin123",
    "staff": "staff123"
}

# -------- LOGIN --------
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# -------- DASHBOARD --------
else:
    st.subheader("📊 Inventory Dashboard")
    st.write(f"Logged in as **{st.session_state.username}**")

    with st.form("inventory_form"):
        item = st.text_input("Item name", key="item")
        qty = st.number_input("Quantity", min_value=1, step=1, key="qty")
        action = st.selectbox("Action", ["IN", "OUT"], key="action")
        submit = st.form_submit_button("Update Inventory")

    if submit:
        change = qty if action == "IN" else -qty

        st.session_state.inventory.append({
            "Item": item,
            "Change": change,
            "Action": action,
            "User": st.session_state.username,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        st.success("Inventory updated")

    # Display data
    if st.session_state.inventory:
        df = pd.DataFrame(st.session_state.inventory)

        st.subheader("📋 Inventory Log")
        st.dataframe(df, use_container_width=True)

        st.subheader("📦 Current Stock")
        stock = df.groupby("Item")["Change"].sum()
        st.bar_chart(stock)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
