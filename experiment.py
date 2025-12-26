import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🧪 A/B Experiment Tracker")

# ---------- SESSION STATE ----------
if "experiments" not in st.session_state:
    st.session_state.experiments = []

# ---------- LOG USER EVENT ----------
with st.form("ab_event_form"):
    st.subheader("📥 Log User Event")

    variant = st.selectbox("Variant", ["A", "B"])
    converted = st.selectbox("Conversion", ["Yes", "No"])

    submit = st.form_submit_button("Log Event")

if submit:
    st.session_state.experiments.append({
        "Variant": variant,
        "Converted": 1 if converted == "Yes" else 0,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success("Event logged")

# ---------- DISPLAY RESULTS ----------
if st.session_state.experiments:
    df = pd.DataFrame(st.session_state.experiments)

    st.subheader("📋 Experiment Events")
    st.dataframe(df, use_container_width=True)

    # Metrics per variant
    summary = (
        df.groupby("Variant")
        .agg(
            Visitors=("Converted", "count"),
            Conversions=("Converted", "sum")
        )
    )

    summary["Conversion Rate (%)"] = (
        summary["Conversions"] / summary["Visitors"] * 100
    ).round(2)

    st.subheader("📊 A/B Results")
    st.dataframe(summary, use_container_width=True)

    st.subheader("📈 Conversion Rate Comparison")
    st.bar_chart(summary["Conversion Rate (%)"])

else:
    st.info("No experiment data yet")
