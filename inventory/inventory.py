import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📦 Real-Time Inventory Monitoring")

# Initialize inventory in session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# Input section
st.subheader("Update Inventory")

item_name = st.text_input("Item Name")
quantity = st.number_input("Quantity", min_value=1, step=1)
action = st.selectbox("Action", ["IN (Restock)", "OUT (Sale)"])

if st.button("Update Stock"):
    if item_name:
        record = {
            "Item": item_name,
            "Quantity": quantity if action == "IN (Restock)" else -quantity,
            "Action": action,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.inventory.append(record)
        st.success("Inventory updated!")
    else:
        st.error("Item name is required")

# Display inventory log
st.subheader("Inventory Log")

if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    st.dataframe(df)

    # Current stock calculation
    stock = df.groupby("Item")["Quantity"].sum()

    st.subheader("Current Stock Levels")
    st.bar_chart(stock)
else:
    st.info("No inventory updates yet.")
