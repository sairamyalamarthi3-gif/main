import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# MANUAL LOGIN CREDENTIALS
# =========================
USERS = {
    "admin": "admin123",
    "user1": "password1"
}

# =========================
# SESSION STATE SETUP
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(
        columns=["user_id", "order_id", "timestamp", "status"]
    )

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title("📦 Order Management Dashboard")

    if st.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    # -------------------------
    # ADD ORDER (USER INPUT)
    # -------------------------
    st.subheader("➕ Create New Order")

    user_id = st.text_input("User ID")
    order_id = st.text_input("Order ID")
    status = st.selectbox("Order Status", ["Pending", "Processing"])

    if st.button("Add Order"):
        if user_id.strip() == "" or order_id.strip() == "":
            st.error("User ID and Order ID are required")
        else:
            new_row = pd.DataFrame([{
                "user_id": user_id,
                "order_id": order_id,
                "timestamp": datetime.now(),
                "status": status
            }])

            st.session_state.orders = pd.concat(
                [st.session_state.orders, new_row],
                ignore_index=True
            )

            st.success("Order added successfully ✅")

    # -------------------------
    # UPDATE STATUS
    # -------------------------
    st.subheader("🔄 Update Order Status")

    if not st.session_state.orders.empty:
        selectable_orders = st.session_state.orders[
            st.session_state.orders["status"] != "Completed"
        ]

        if not selectable_orders.empty:
            selected = st.selectbox(
                "Select Order",
                selectable_orders["order_id"]
            )

            new_status = st.selectbox(
                "New Status",
                ["Pending", "Processing", "Completed"]
            )

            if st.button("Update Status"):
                st.session_state.orders.loc[
                    st.session_state.orders["order_id"] == selected,
                    "status"
                ] = new_status

                st.success("Order status updated ✅")
        else:
            st.info("No active orders to update.")
    else:
        st.info("No orders available.")

    # -------------------------
    # METRICS
    # -------------------------
    st.subheader("📊 Order Summary")

    counts = st.session_state.orders["status"].value_counts()
    st.metric("🕒 Pending", counts.get("Pending", 0))
    st.metric("⚙️ Processing", counts.get("Processing", 0))
    st.metric("✅ Completed", counts.get("Completed", 0))

    # -------------------------
    # ALERT
    # -------------------------
    if counts.get("Pending", 0) > 5:
        st.error("⚠️ Too many pending orders!")

    # -------------------------
    # TABLE
    # -------------------------
    st.subheader("📋 Orders Table")
    st.dataframe(st.session_state.orders, use_container_width=True)

# =========================
# APP FLOW
# =========================
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
