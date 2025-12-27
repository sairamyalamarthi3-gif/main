import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🛠 Batch Job Health Tracker")

# -------- SESSION STATE --------
if "job_health_logs" not in st.session_state:
    st.session_state.job_health_logs = []

# -------- JOB UPDATE FORM --------
with st.form("job_form"):
    st.subheader("Update Job Health")

    job_name = st.text_input("Job Name")

    status = st.selectbox(
        "Job Status",
        ["⏳ Running", "✅ Success", "❌ Failed"]
    )

    health = st.selectbox(
        "Job Health",
        ["🟢 Healthy", "🟡 Degraded", "🔴 Unhealthy"]
    )

    submit = st.form_submit_button("Save Update")

if submit and job_name:
    st.session_state.job_health_logs.append({
        "Job Name": job_name,
        "Status": status,
        "Health": health,
        "Timestamp": datetime.now()
    })
    st.success("Job health record saved")

# -------- DASHBOARD --------
if st.session_state.job_health_logs:
    df = pd.DataFrame(st.session_state.job_health_logs)

    # -------- LATEST HEALTH PER JOB --------
    latest_df = (
        df.sort_values("Timestamp")
          .groupby("Job Name", as_index=False)
          .last()
    )

    latest_df["Timestamp"] = latest_df["Timestamp"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.subheader("📋 Latest Job Health")
    st.dataframe(latest_df, use_container_width=True)

    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Healthy Jobs", (latest_df["Health"] == "🟢 Healthy").sum())
    col2.metric("🟡 Degraded Jobs", (latest_df["Health"] == "🟡 Degraded").sum())
    col3.metric("🔴 Unhealthy Jobs", (latest_df["Health"] == "🔴 Unhealthy").sum())

    # -------- ALERTS --------
    if (latest_df["Health"] == "🔴 Unhealthy").any():
        st.error("🚨 One or more jobs are unhealthy")
    elif (latest_df["Health"] == "🟡 Degraded").any():
        st.warning("⚠️ Some jobs are degraded")
    else:
        st.success("✅ All jobs healthy")

    # -------- FULL HISTORY --------
    with st.expander("📜 View Full Job Health History"):
        history_df = df.copy()
        history_df["Timestamp"] = history_df["Timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        st.dataframe(history_df, use_container_width=True)

else:
    st.info("No job health records yet")
