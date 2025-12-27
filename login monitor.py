import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🔐 Login Failure Monitoring Dashboard")

# -------- SESSION STATE --------
if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

# -------- LOGIN SIMULATION --------
with st.form("login_form"):
    st.subheader("Simulate Login Attempt")

    username = st.text_input("Username")
    success = st.selectbox("Login Result", ["Success", "Failure"])

    submit = st.form_submit_button("Submit")

if submit and username:
    st.session_state.login_logs.append({
        "Username": username,
        "Result": success,
        "Timestamp": datetime.now()
    })
    st.success("Login attempt recorded")

# -------- DASHBOARD --------
if st.session_state.login_logs:
    df = pd.DataFrame(st.session_state.login_logs)

    # Count failures per user
    failure_counts = (
        df[df["Result"] == "Failure"]
        .groupby("Username")
        .size()
        .reset_index(name="Failed Attempts")
    )

    # SLA / Security tiers
    def risk_level(count):
        if count <= 2:
            return "🟢 Normal"
        elif count <= 4:
            return "🟡 Suspicious"
        else:
            return "🔴 Locked"

    failure_counts["Risk Level"] = failure_counts["Failed Attempts"].apply(risk_level)

    st.subheader("📋 User Login Risk Status")
    st.dataframe(failure_counts, use_container_width=True)

    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Normal Users", (failure_counts["Risk Level"] == "🟢 Normal").sum())
    col2.metric("🟡 Suspicious Users", (failure_counts["Risk Level"] == "🟡 Suspicious").sum())
    col3.metric("🔴 Locked Users", (failure_counts["Risk Level"] == "🔴 Locked").sum())

    # -------- ALERTS --------
    if (failure_counts["Risk Level"] == "🔴 Locked").any():
        st.error("🚨 Accounts locked due to repeated failures")
    elif (failure_counts["Risk Level"] == "🟡 Suspicious").any():
        st.warning("⚠️ Suspicious login activity detected")
    else:
        st.success("✅ Login activity normal")

else:
    st.info("No login attempts yet")
