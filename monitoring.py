import streamlit as st

# =========================
# SESSION STATE SETUP
# =========================
if "users" not in st.session_state:
    st.session_state.users = {}   # stores {username: password}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# =========================
# REGISTER PAGE
# =========================
def register_page():
    st.title("📝 Register")

    new_user = st.text_input("Create User ID")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if new_user == "" or new_pass == "":
            st.error("All fields are required")
        elif new_user in st.session_state.users:
            st.error("User already exists")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("User registered successfully ✅")
            st.info("You can now login")

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.title("🔐 Login")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if st.session_state.users.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials")

# =========================
# DASHBOARD
# =========================
def dashboard():
    st.title("📊 Dashboard")
    st.write(f"Welcome **{st.session_state.current_user}** 👋")

    if st.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

# =========================
# APP NAVIGATION
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if st.session_state.logged_in:
    dashboard()
else:
    if menu == "Register":
        register_page()
    else:
        login_page()
