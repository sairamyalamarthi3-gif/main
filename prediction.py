import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.title("⚡ Model Prediction Latency Monitor")

# ---------- SESSION STATE ----------
if "latency_logs" not in st.session_state:
    st.session_state.latency_logs = []

# ---------- SIMULATE PREDICTION ----------
with st.form("latency_form"):
    st.subheader("📡 Simulate Model Prediction")

    model_name = st.selectbox("Model", ["FraudModel", "Recommender", "ChurnModel"])
    simulate = st.form_submit_button("Run Prediction")

if simulate:
    latency_ms = random.randint(50, 800)  # simulate latency
    st.session_state.latency_logs.append({
        "Model": model_name,
        "Latency_ms": latency_ms,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success(f"Prediction completed in {latency_ms} ms")

# ---------- DASHBOARD ----------
if st.session_state.latency_logs:
    df = pd.DataFrame(st.session_state.latency_logs)

    st.subheader("📋 Latency Logs")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Average Latency by Model")
    avg_latency = df.groupby("Model")["Latency_ms"].mean().round(2)
    st.bar_chart(avg_latency)

    # ---------- SLA MONITOR ----------
    st.subheader("🚨 SLA Monitoring")

    SLA_THRESHOLD = 500  # ms
    slow_requests = df[df["Latency_ms"] > SLA_THRESHOLD]

    st.metric("Total Requests", len(df))
    st.metric("SLA Breaches", len(slow_requests))

    if not slow_requests.empty:
        st.warning("Some requests exceeded SLA")
        st.dataframe(slow_requests, use_container_width=True)
    else:
        st.success("All requests within SLA")

else:
    st.info("No predictions logged yet")
