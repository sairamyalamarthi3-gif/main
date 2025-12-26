import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🕒 Employee Attendance Tracker")

# -------- SESSION STATE --------
if "attendance" not in st.session_state:
    st.session_state.attendance = []

# -------- CHECK IN --------
with st.form("check_in_form"):
    st.subheader("✅ Check In")
    emp_name = st.text_input("Employee Name", key="in_name")
    check_in_btn = st.form_submit_button("Check In")

if check_in_btn and emp_name:
    st.session_state.attendance.append({
        "Employee": emp_name,
        "Check In": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Check Out": None
    })
    st.success("Checked in successfully")

# -------- CHECK OUT --------
st.subheader("🚪 Check Out")

df = pd.DataFrame(st.session_state.attendance)

if not df.empty:
    active_employees = df[df["Check Out"].isna()]["Employee"].tolist()

    if active_employees:
        selected_emp = st.selectbox("Select Employee", active_employees)
        if st.button("Check Out"):
            for record in st.session_state.attendance:
                if record["Employee"] == selected_emp and record["Check Out"] is None:
                    record["Check Out"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            st.success("Checked out successfully")
    else:
        st.info("No active employees")

# -------- DISPLAY TABLE --------
if st.session_state.attendance:
    st.subheader("📋 Attendance Log")
    df = pd.DataFrame(st.session_state.attendance)
    st.dataframe(df, use_container_width=True)

    present_count = df[df["Check Out"].isna()].shape[0]
    st.metric("Employees Currently Present", present_count)
else:
    st.info("No attendance records yet")
