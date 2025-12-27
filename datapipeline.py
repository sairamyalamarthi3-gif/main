import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("🕒 Data Pipeline Freshness Monitor")

# ---------- SESSION STATE ----------
if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []

# ---------- SIMULATE PIPELINE RUN ----------
with st.form("pipeline_form"):
    st.subheader("⚙️ Simulate Pipeline Update")

    pipeline_name = st.selectbox(
        "Pipeline",
        ["User Events ETL", "Sales Aggregation", "Feature Store Update"]
    )

    run_pipeline = st.form_submit_button("Run Pipeline")

if run_pipeline:
    st.session_state.pipeline_logs.append({
        "Pipeline": pipeline_name,
        "Last Updated": datetime.now()
    })
    st.success("Pipeline run logged")

# ---------- DASHBOARD ----------
if st.session_state.pipeline_logs:
    df = pd.DataFrame(st.session_state.pipeline_logs)

    # Keep latest update per pipeline
    latest_df = df.sort_values("Last Updated").groupby(
        "Pipeline", as_index=False
    ).last()

    # Calculate freshness
    now = datetime.now()
    latest_df["Minutes Since Update"] = (
        now - latest_df["Last Updated"]
    ).dt.total_seconds() / 60

    st.subheader("📋 Pipeline Status")
    st.dataframe(
        latest_df.assign(
            **{"Last Updated": latest_df["Last Updated"].dt.strftime("%Y-%m-%d %H:%M:%S")}
        ),
        use_container_width=True
    )

    # ---------- FRESHNESS CHECK ----------
    st.subheader("🚦 Freshness Check")

    FRESHNESS_THRESHOLD = 15  # minutes

    stale = latest_df[latest_df["Minutes Since Update"] > FRESHNESS_THRESHOLD]

    st.metric("Total Pipelines", len(latest_df))
    st.metric("Stale Pipelines", len(stale))

    if not stale.empty:
        st.error("⚠️ Some pipelines are stale")
        st.dataframe(stale[["Pipeline", "Minutes Since Update"]])
    else:
        st.success("✅ All pipelines are fresh")

else:
    st.info("No pipeline runs recorded yet")
