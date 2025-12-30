import streamlit as st
from datetime import datetime

# =========================
# SESSION STATE SETUP
# =========================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "inventory" not in st.session_state:
    st.session_state.inventory = {}  
    # {item_name: quantity}

if "sales" not in st.session_state:
    st.session_state.sales = []  
    # list of {item, qty, price, total, date}


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

    tab1, tab2, tab3 = st.tabs(
        ["📦 Item Entry", "💰 Sell Items", "📊 End of Day"]
    )

    # ---------- ITEM ENTRY ----------
    with tab1:
        st.subheader("Add Items to Store")

        item = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=1, step=1)

        if st.button("Add Item"):
            if item:
                st.session_state.inventory[item] = (
                    st.session_state.inventory.get(item, 0) + qty
                )
                st.success(f"{qty} units of {item} added")
            else:
                st.error("Item name required")

        st.write("### Current Inventory")
        st.write(st.session_state.inventory)

    # ---------- SELL ITEMS ----------
    with tab2:
        st.subheader("Sell Items")

        if not st.session_state.inventory:
            st.info("No items in inventory")
        else:
            item = st.selectbox(
                "Select Item", list(st.session_state.inventory.keys())
            )

            available = st.session_state.inventory[item]
            st.write(f"Available Stock: {available}")

            sell_qty = st.number_input(
                "Quantity to Sell", min_value=1, max_value=available, step=1
            )

            price = st.number_input(
                "Price per Item (£)", min_value=0.01, step=0.5
            )

            if st.button("Sell"):
                total = sell_qty * price

                st.session_state.inventory[item] -= sell_qty

                sale = {
                    "item": item,
                    "quantity": sell_qty,
                    "price": price,
                    "total": total,
                    "date": datetime.now().date()
                }

                st.session_state.sales.append(sale)
                st.success(f"Sold {sell_qty} {item} for £{total:.2f}")

    # ---------- END OF DAY ----------
    with tab3:
        st.subheader("Daily Sales Summary")

        today = datetime.now().date()
        today_sales = [
            s for s in st.session_state.sales if s["date"] == today
        ]

        if today_sales:
            total_revenue = sum(s["total"] for s in today_sales)

            for s in today_sales:
                st.write(
                    f"{s['item']} | Qty: {s['quantity']} | "
                    f"£{s['total']:.2f}"
                )

            st.success(f"💷 Total Revenue Today: £{total_revenue:.2f}")
        else:
            st.info("No sales today")

        if st.button("Exit / Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()


# =========================
# MAIN APP
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if st.session_state.logged_in:
    dashboard()
else:
    if menu == "Register":
        register()
    else:
        login()
