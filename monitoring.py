import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

st.title("📦 Real-Time Order Queue Monitoring")

# ------------------------
# CONFIG
# ------------------------
PENDING_THRESHOLD = 5
REFRESH_SECONDS = 4

# ------------------------
# SESSION STATE
# ------------------------
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(
        columns=["order_id", "timestamp", "status"]
    )

# ------------------------
# SIMULATE NEW ORDER
# ------------------------
def generate_order():
    return {
        "order_id": random.randint(1000, 9999),
        "timestamp": datetime.now(),
        "status": random.choice(["Pending", "Processing", "Completed"])
    }

# Add new order automatically
new_order = generate_order()
st.session_state.orders = pd.concat(
    [st.session_state.orders, pd.DataFrame([new_order])],
    ignore_index=True
)

# ------------------------
# DASHBOARD METRICS
# ------------------------
status_counts = st.session_state.orders["status"].value_counts()

pending = status_counts.get("Pending", 0)
processing = status_counts.get("Processing", 0)
completed = status_counts.get("Completed", 0)

st.subheader("📊 Current Order Status")

col1, col2, col3 = st.columns(3)
col1.metric("🕒 Pending", pending)
col2.metric("⚙️ Processing", processing)
col3.metric("✅ Completed", completed)

# ------------------------
# WARNING
# ------------------------
if pending > PENDING_THRESHOLD:
    st.error("⚠️ Order backlog is high! Immediate action required.")
else:
    st.success("Order queue is healthy ✅")

# ------------------------
# DATA TABLE
# ------------------------
st.subheader("📋 Live Order Feed")
st.dataframe(st.session_state.orders.tail(10))

# ------------------------
# AUTO REFRESH
# ------------------------
time.sleep(REFRESH_SECONDS)
st.rerun()
