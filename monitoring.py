import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Order Queue Monitoring (Manual Input)")

PENDING_THRESHOLD = 5

# ------------------------
# SESSION STATE
# ------------------------
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(
        columns=["order_id", "timestamp", "status"]
    )

# ------------------------
# ADD NEW ORDER
# ------------------------
st.subheader("➕ Add New Order")

order_id = st.text_input("Order ID")
status = st.selectbox("Order Status", ["Pending", "Processing"])

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
# UPDATE ORDER STATUS
# ------------------------
st.subheader("🔄 Update Order Status")

if not st.session_state.orders.empty:
    updatable_orders = st.session_state.orders[
        st.session_state.orders["status"].isin(["Pending", "Processing"])
    ]

    if not updatable_orders.empty:
        selected_order = st.selectbox(
            "Select Order to Mark as Completed",
            updatable_orders["order_id"]
        )

        if st.button("Mark as Completed ✅"):
            st.session_state.orders.loc[
                st.session_state.orders["order_id"] == selected_order,
                "status"
            ] = "Completed"

            st.success(f"Order {selected_order} marked as Completed!")
    else:
        st.info("No Pending or Processing orders available to update.")
else:
    st.info("No orders available yet.")

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
# ALERT
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
