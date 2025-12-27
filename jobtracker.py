import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🛠 Batch Job Status Tracker")

# -------- SESSION STATE --------
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# -------- JOB CREATION --------
with st.form("job_form"):
    st.subheader("Create / Update Job")

    job_name = st.text_input("Job Name")
    status = st.selectbox(
        "Job Status",
        ["⏳ Running", "✅ Success", "❌ Failed"]
    )

    submit = st.form_submit_button("Save")

if submit and job_name:
    st.session_state.jobs.append({
        "Job Name": job_name,
        "Status": status,
        "Updated At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success("Job status updated")

# -------- DASHBOARD --------
if st.session_state.jobs:
    df = pd.DataFrame(st.session_state.jobs)

    # Show latest status per job
    df = df.groupby("Job Name", as_index=False).last()

    st.subheader("📋 Job Status Overview")
    st.dataframe(df, use_container_width=True)

    # -------- METRICS --------
    col1, col2, col3 = st.columns(3)
    col1.metric("⏳ Running", (df["Status"] == "⏳ Running").sum())
    col2.metric("✅ Success", (df["Status"] == "✅ Success").sum())
    col3.metric("❌ Failed", (df["Status"] == "❌ Failed").sum())

    # -------- ALERT --------
    if (df["Status"] == "❌ Failed").any():
        st.error("🚨 One or more jobs have failed")
    else:
        st.success("All jobs healthy")

else:
    st.info("No jobs recorded yet")
