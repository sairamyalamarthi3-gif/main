import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.title("📊 Data Volume Anomaly Monitor")

# ---------- SESSION STATE ----------
if "volume_logs" not in st.session_state:
    st.session_state.volume_logs = []

# ---------- SIMULATE DATA INGEST ----------
with st.form("volume_form"):
    st.subheader("Simulate Daily Data Ingest")

    pipeline = st.selectbox(
        "Pipeline Name",
        ["Orders Pipeline", "User Events Pipeline", "Logs Pipeline"]
    )

    records = st.number_input(
        "Records Ingested",
        min_value=0,
        value=random.randint(800, 1200),
        step=50
    )

    submit = st.form_submit_button("Record Ingest")

if submit:
    st.session_state.volume_logs.append({
        "Pipeline": pipeline,
        "Records": records,
        "Date": datetime.now().date()
    })
    st.success("Data volume recorded")

# ---------- DASHBOARD ----------
if st.session_state.volume_logs:
    df = pd.DataFrame(st.session_state.volume_logs)

    # Average volume per pipeline
    avg_df = (
        df.groupby("Pipeline")["Records"]
          .mean()
          .reset_index(name="Avg Records")
    )

    latest_df = (
        df.groupby("Pipeline", as_index=False)
          .last()
          .merge(avg_df, on="Pipeline")
    )

    # Anomaly logic
    def volume_status(row):
        lower = row["Avg Records"] * 0.8
        upper = row["Avg Records"] * 1.2
        if row["Records"] < lower or row["Records"] > upper:
            return "🔴 Anomaly"
        return "🟢 Normal"

    latest_df["Status"] = latest_df.apply(volume_status, axis=1)

    st.subheader("📋 Latest Data Volume Status")
    st.dataframe(latest_df, use_container_width=True)

    # ---------- METRICS ----------
    col1, col2 = st.columns(2)
    col1.metric("🟢 Normal Pipelines", (latest_df["Status"] == "🟢 Normal").sum())
    col2.metric("🔴 Anomalies", (latest_df["Status"] == "🔴 Anomaly").sum())

    # ---------- ALERT ----------
    if (latest_df["Status"] == "🔴 Anomaly").any():
        st.error("🚨 Data volume anomaly detected")
    else:
        st.success("✅ Data volumes within expected range")

    # ---------- HISTORY ----------
    with st.expander("📜 Volume History"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("No data volume records yet")
