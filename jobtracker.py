import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🛠 Advanced Batch Job Health Tracker")

# ---------- SESSION STATE ----------
if "job_logs" not in st.session_state:
    st.session_state.job_logs = []

# ---------- JOB UPDATE FORM ----------
with st.form("job_form"):
    st.subheader("Update Job Run")

    job_name = st.text_input("Job Name")
    status = st.selectbox(
        "Job Status",
        ["⏳ Running", "✅ Success", "❌ Failed"]
    )
    duration = st.number_input(
        "Duration (seconds)", min_value=0, step=10
    )
    failure_reason = st.text_input(
        "Failure Reason (if failed)"
    )

    submit = st.form_submit_button("Save Job Run")

if submit and job_name:
    st.session_state.job_logs.append({
        "Job Name": job_name,
        "Status": status,
        "Duration (sec)": duration,
        "Failure Reason": failure_reason if status == "❌ Failed" else "",
        "Timestamp": datetime.now()
    })
    st.success("Job run recorded")

# ---------- DASHBOARD ----------
if st.session_state.job_logs:
    df = pd.DataFrame(st.session_state.job_logs)

    # ---------- AUTO HEALTH LOGIC ----------
    df = df.sort_values("Timestamp")

    def compute_health(job_df):
        last_two = job_df.tail(2)
        if (last_two["Status"] == "❌ Failed").sum() >= 2:
            return "🔴 Unhealthy"
        elif job_df.iloc[-1]["Status"] == "❌ Failed":
            return "🟡 Degraded"
        else:
            return "🟢 Healthy"

    health_map = (
        df.groupby("Job Name")
          .apply(compute_health)
          .reset_index(name="Health")
    )

    # ---------- LATEST STATUS ----------
    latest = (
        df.groupby("Job Name", as_index=False)
          .last()
          .merge(health_map, on="Job Name")
    )

    latest["Timestamp"] = latest["Timestamp"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ---------- FILTER ----------
    st.subheader("🔍 Filter Jobs")
    selected_job = st.selectbox(
        "Select Job",
        ["All"] + latest["Job Name"].tolist()
    )

    if selected_job != "All":
        latest = latest[latest["Job Name"] == selected_job]

    # ---------- DISPLAY ----------
    st.subheader("📋 Latest Job Health")
    st.dataframe(latest, use_container_width=True)

    # ---------- METRICS ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Healthy", (latest["Health"] == "🟢 Healthy").sum())
    col2.metric("🟡 Degraded", (latest["Health"] == "🟡 Degraded").sum())
    col3.metric("🔴 Unhealthy", (latest["Health"] == "🔴 Unhealthy").sum())

    # ---------- ALERTS ----------
    if (latest["Health"] == "🔴 Unhealthy").any():
        st.error("🚨 Jobs failing repeatedly!")
    elif (latest["Health"] == "🟡 Degraded").any():
        st.warning("⚠️ Some jobs failed recently")
    else:
        st.success("✅ All jobs healthy")

    # ---------- HISTORY ----------
    with st.expander("📜 Full Job Run History"):
        hist = df.copy()
        hist["Timestamp"] = hist["Timestamp"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        st.dataframe(hist, use_container_width=True)

        # ---------- CSV EXPORT ----------
        csv = hist.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download History as CSV",
            csv,
            "job_history.csv",
            "text/csv"
        )

else:
    st.info("No job runs recorded yet")
