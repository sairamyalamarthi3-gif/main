import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Employee Login Dashboard")

##Step1 Sample Employess

employees = ["Alice","Bob","Charlie"]

##Step 2
##Initialize session state to track logins
if "login_data" not in st.session_state:
  st.session_state.login_data = pd.DataFrame(columns = ["Employee","Time","Status"])

##Step 3 Employee login Simulation
selected_employee = st.selectbox("Select Employee to Login", employees)
if st.button("Login"):
  new_row = {
    "Employee": selected_employee,
    "Time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Status": "Success"
  }
  st.session_state.login_data = pd.concat(
        [st.session_state.login_data, pd.DataFrame([new_row])],
        ignore_index=True
    )
  st.success(f"{selected_employee} logged in successfully!")

# Step 4: Show real-time login table
st.subheader("Login History")
st.dataframe(st.session_state.login_data)

# Step 5: Optional: show count of logins per employee
st.subheader("Login Counts")
login_counts = st.session_state.login_data["Employee"].value_counts()
st.bar_chart(login_counts)
