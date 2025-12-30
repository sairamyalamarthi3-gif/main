import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =========================
# FILE PATHS
# =========================
INVENTORY_FILE = "inventory.csv"
SALES_FILE = "sales.csv"

# =========================
# INITIAL FILE SETUP
# =========================
if not os.path.exists(INVENTORY_FILE):
    pd.DataFrame(
        columns=["item", "quantity", "cost_price"]
    ).to_csv(INVENTORY_FILE, index=False)

if not os.path.exists(SALES_FILE):
    pd.DataFrame(
        columns=["date", "item", "quantity", "sell_price", "cost_price", "revenue", "profit"]
    ).to_csv(SALES_FILE, index=False)

# =========================
# SESSION STATE
# =========================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# =========================
# REGISTER
# =========================
def register():
    st.title("📝 Register")

    user = st.text_input("Create User ID")
    pwd = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if not user or not pwd:
            st.error("All fields required")
        elif user in st.session_state.users:
            st.error("User already exists")
        else:
            st.session_state.users[user] = pwd
            st.success("Registration successful ✅")

# =========================
# LOGIN
# =========================
def login():
    st.title("🔐 Login")

    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if st.session_state.users.get(user) == pwd:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.rerun()
        else:
            st.error("Invalid credentials")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title("🏪 Store Management Dashboard")
    st.write(f"Welcome **{st.session_state.current_user}** 👋")

    inventory_df = pd.read_csv(INVENTORY_FILE)
    sales_df = pd.read_csv(SALES_FILE)

    tab1, tab2, tab3 = st.tabs(
        ["📦 Item Entry", "💰 Sell Items", "📊 Sales History"]
    )

    # ---------- ITEM ENTRY ----------
    with tab1:
        st.subheader("Add Items to Inventory")

        item = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=1, step=1)
        cost_price = st.number_input("Cost Price (£)", min_value=0.01, step=0.5)

        if st.button("Add / Update Item"):
            if item:
                if item in inventory_df["item"].values:
                    inventory_df.loc[
                        inventory_df["item"] == item, "quantity"
                    ] += qty
                else:
                    inventory_df = pd.concat([
                        inventory_df,
                        pd.DataFrame([{
                            "item": item,
                            "quantity": qty,
                            "cost_price": cost_price
                        }])
                    ])
                inventory_df.to_csv(INVENTORY_FILE, index=False)
                st.success("Inventory updated ✅")
            else:
                st.error("Item name required")

        st.write("### Current Inventory")
        st.dataframe(inventory_df)

    # ---------- SELL ITEMS ----------
    with tab2:
        st.subheader("Sell Items")

        if inventory_df.empty:
            st.info("No inventory available")
        else:
            item = st.selectbox("Select Item", inventory_df["item"])
            available = inventory_df.loc[
                inventory_df["item"] == item, "quantity"
            ].values[0]
            cost_price = inventory_df.loc[
                inventory_df["item"] == item, "cost_price"
            ].values[0]

            st.write(f"Available Stock: {available}")
            sell_qty = st.number_input(
                "Quantity to Sell", min_value=1, max_value=int(available), step=1
            )
            sell_price = st.number_input(
                "Selling Price (£)", min_value=0.01, step=0.5
            )

            if st.button("Sell"):
                revenue = sell_qty * sell_price
                profit = (sell_price - cost_price) * sell_qty

                inventory_df.loc[
                    inventory_df["item"] == item, "quantity"
                ] -= sell_qty

                sale = {
                    "date": datetime.now().date(),
                    "item": item,
                    "quantity": sell_qty,
                    "sell_price": sell_price,
                    "cost_price": cost_price,
                    "revenue": revenue,
                    "profit": profit
                }

                sales_df = pd.concat([
                    sales_df,
                    pd.DataFrame([sale])
                ])

                inventory_df.to_csv(INVENTORY_FILE, index=False)
                sales_df.to_csv(SALES_FILE, index=False)

                st.success(f"Sold successfully 💰 Revenue: £{revenue:.2f}")

    # ---------- SALES HISTORY ----------
    with tab3:
        st.subheader("Sales History")

        if sales_df.empty:
            st.info("No sales recorded yet")
        else:
            sales_df["date"] = pd.to_datetime(sales_df["date"])
            selected_date = st.date_input(
                "Select Date",
                value=datetime.now().date()
            )

            daily_sales = sales_df[
                sales_df["date"].dt.date == selected_date
            ]

            if not daily_sales.empty:
                st.dataframe(daily_sales)

                st.success(
                    f"Total Revenue: £{daily_sales['revenue'].sum():.2f}"
                )
                st.info(
                    f"Total Profit: £{daily_sales['profit'].sum():.2f}"
                )
            else:
                st.warning("No sales on this date")

        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

# =========================
# MAIN
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if st.session_state.logged_in:
    dashboard()
else:
    if menu == "Register":
        register()
    else:
        login()
