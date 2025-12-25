import streamlit as st

st.title("🔐 Login Page Example")

# Initialize login state in session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button logic
if st.button("Login"):
    if username == "admin" and password == "1234":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

# Show dashboard only if logged in
if st.session_state.logged_in:
    st.header("Dashboard")
    st.write("Welcome to the dashboard!")
  
    
