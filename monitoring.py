import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Order Queue Monitoring (Manual Input)")

# ------------------------
# CONFIG
# ------------------------
PENDING_THRESHOLD = 5

# ------------------------
# SESSION STATE
# ------------------------
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(
        columns=["order_id", "timestamp", "status"]
    )

# ------------------------
# MANUAL INPUT SECTION
# ------------------------
st.subheader("➕ Add New Order")

order_id = st.text_input("Order ID")
status = st.selectbox(
    "Order Status",
    ["Pending", "Processing", "Completed"]
)

if st.button("Add Order"):
    if order_id.strip() == "":
        st.error("Order ID cannot be empty")
    else:
        new_order = {
            "order_id": order_id,
            "timestamp": datetime.now(),
            "status": status
        }

        st.session_state.orders = pd.concat(
            [st.session_state.orders, pd.DataFrame([new_order])],
            ignore_index=True
        )

        st.success("Order added successfully!")

# ------------------------
# DASHBOARD METRICS
# ------------------------
st.subheader("📊 Order Status Summary")

status_counts = st.session_state.orders["status"].value_counts()

pending = status_counts.get("Pending", 0)
processing = status_counts.get("Processing", 0)
completed = status_counts.get("Completed", 0)

col1, col2, col3 = st.columns(3)
col1.metric("🕒 Pending", pending)
col2.metric("⚙️ Processing", processing)
col3.metric("✅ Completed", completed)

# ------------------------
# ALERT LOGIC
# ------------------------
st.subheader("🚨 Alerts")

if pending > PENDING_THRESHOLD:
    st.error("⚠️ High number of pending orders! Please take action.")
else:
    st.success("Order queue is under control ✅")

# ------------------------
# DATA TABLE
# ------------------------
st.subheader("📋 Order List")
st.dataframe(st.session_state.orders)
