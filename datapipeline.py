import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📊 Data Pipeline SLA Monitor")

# ---------------- SESSION STATE ----------------
if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []

# ---------------- SLA THRESHOLDS ----------------
GREEN_LIMIT = 1     # minutes
YELLOW_LIMIT = 3   # minutes

# ---------------- SIMULATE PIPELINE RUN ----------------
with st.form("pipeline_form"):
    st.subheader("⚙️ Simulate Pipeline Run")

    pipeline_name = st.selectbox(
        "Pipeline Name",
        ["User Events ETL", "Sales Aggregation", "Feature Store Update"]
    )

    submit = st.form_submit_button("Run Pipeline")

if submit:
    st.session_state.pipeline_logs.append({
        "Pipeline": pipeline_name,
        "Last Updated": datetime.now()
    })
    st.success(f"{pipeline_name} updated")

# ---------------- DASHBOARD ----------------
if st.session_state.pipeline_logs:
    df = pd.DataFrame(st.session_state.pipeline_logs)

    # Keep only latest run per pipeline
    df = df.sort_values("Last Updated").groupby(
        "Pipeline", as_index=False
    ).last()

    # Calculate freshness
    now = datetime.now()
    df["Minutes Since Update"] = (
        now - df["Last Updated"]
    ).dt.total_seconds() / 60

    # SLA Status logic
    def sla_status(minutes):
        if minutes <= GREEN_LIMIT:
            return "🟢 Green"
        elif minutes <= YELLOW_LIMIT:
            return "🟡 Yellow"
        else:
            return "🔴 Red"

    df["SLA Status"] = df["Minutes Since Update"].apply(sla_status)

    # Format time
    df["Last Updated"] = df["Last Updated"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["Minutes Since Update"] = df["Minutes Since Update"].round(1)

    st.subheader("📋 Pipeline SLA Status")
    st.dataframe(df, use_container_width=True)

    # ---------------- METRICS ----------------
    green = (df["SLA Status"] == "🟢 Green").sum()
    yellow = (df["SLA Status"] == "🟡 Yellow").sum()
    red = (df["SLA Status"] == "🔴 Red").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Green", green)
    col2.metric("🟡 Yellow", yellow)
    col3.metric("🔴 Red", red)

    # ---------------- ALERT ----------------
    if red > 0:
        st.error("🚨 Critical SLA breach detected!")
    elif yellow > 0:
        st.warning("⚠️ Some pipelines nearing SLA limits")
    else:
        st.success("✅ All pipelines within SLA")

else:
    st.info("No pipeline runs yet. Simulate a pipeline run above.")
