import streamlit as st
import pandas as pd
from datetime import datetime, time

st.title("🕘 Employee Attendance Monitoring")

# ------------------------
# CONFIG
# ------------------------
OFFICE_TIME = time(9, 30)

# ------------------------
# SESSION STATE
# ------------------------
if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(
        columns=["employee_id", "checkin_time", "status", "date"]
    )

# ------------------------
# CHECK-IN INPUT
# ------------------------
st.subheader("Employee Check-In")

emp_id = st.text_input("Employee ID")
checkin_time = st.time_input("Check-in Time", value=datetime.now().time())

if st.button("Check In"):
    if emp_id.strip() == "":
        st.error("Employee ID required")
    else:
        status = "⚠️ Late" if checkin_time > OFFICE_TIME else "✅ On Time"

        new_entry = pd.DataFrame([{
            "employee_id": emp_id,
            "checkin_time": checkin_time,
            "status": status,
            "date": datetime.now().date()
        }])

        st.session_state.attendance = pd.concat(
            [st.session_state.attendance, new_entry],
            ignore_index=True
        )

        st.success("Check-in recorded")

# ------------------------
# DASHBOARD
# ------------------------
st.subheader("📊 Today’s Attendance")

today = datetime.now().date()
today_data = st.session_state.attendance[
    st.session_state.attendance["date"] == today
]

if not today_data.empty:
    st.dataframe(today_data)

    total = len(today_data)
    late = len(today_data[today_data["status"] == "⚠️ Late"])
    ontime = total - late

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Present", total)
    col2.metric("⏰ Late", late)
    col3.metric("✅ On Time", ontime)

    if late > 0:
        st.error("⚠️ Some employees are late today")
    else:
        st.success("All employees on time 🎉")
else:
    st.info("No check-ins yet today")
