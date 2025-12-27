import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.title("⚡ API Latency SLA Monitor")

# ---------------- SESSION STATE ----------------
if "api_logs" not in st.session_state:
    st.session_state.api_logs = []

# ---------------- SLA THRESHOLDS ----------------
GREEN_LIMIT = 300
YELLOW_LIMIT = 800

# ---------------- SIMULATE API CALL ----------------
with st.form("api_form"):
    st.subheader("🔁 Simulate API Call")

    api_name = st.selectbox(
        "API Name",
        ["Prediction API", "User Auth API", "Payments API"]
    )

    submit = st.form_submit_button("Call API")

if submit:
    latency = random.randint(100, 1200)  # milliseconds

    st.session_state.api_logs.append({
        "API": api_name,
        "Latency (ms)": latency,
        "Timestamp": datetime.now()
    })

    st.success(f"{api_name} responded in {latency} ms")

# ---------------- DASHBOARD ----------------
if st.session_state.api_logs:
    df = pd.DataFrame(st.session_state.api_logs)

    # Latest call per API
    df = df.sort_values("Timestamp").groupby(
        "API", as_index=False
    ).last()

    # SLA logic
    def sla_status(latency):
        if latency <= GREEN_LIMIT:
            return "🟢 Green"
        elif latency <= YELLOW_LIMIT:
            return "🟡 Yellow"
        else:
            return "🔴 Red"

    df["SLA Status"] = df["Latency (ms)"].apply(sla_status)

    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("📋 API SLA Status")
    st.dataframe(df, use_container_width=True)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Green", (df["SLA Status"] == "🟢 Green").sum())
    col2.metric("🟡 Yellow", (df["SLA Status"] == "🟡 Yellow").sum())
    col3.metric("🔴 Red", (df["SLA Status"] == "🔴 Red").sum())

    # ---------------- ALERTS ----------------
    if (df["SLA Status"] == "🔴 Red").any():
        st.error("🚨 High API latency detected!")
    elif (df["SLA Status"] == "🟡 Yellow").any():
        st.warning("⚠️ Some APIs are slow")
    else:
        st.success("✅ All APIs performing well")

else:
    st.info("No API calls yet. Simulate one above.")
