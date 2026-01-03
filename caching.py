import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Streamlit Caching – Step 7 (Visualization Added)")

# -----------------------------
# 1. Cached Data Loader
# -----------------------------
@st.cache_data
def load_data(n_rows: int):
    time.sleep(2)  # simulate slow loading
    df = pd.DataFrame({
        "value": np.random.randn(n_rows),
        "category": np.random.choice(["A", "B", "C"], n_rows)
    })
    return df

# -----------------------------
# 2. Cached Computation
# -----------------------------
@st.cache_data
def compute_stats(df: pd.DataFrame):
    time.sleep(3)  # simulate heavy computation
    return df.groupby("category")["value"].agg(["mean", "std", "count"])

# -----------------------------
# Clear cache button
# -----------------------------
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.warning("Cache cleared!")

# -----------------------------
# User input
# -----------------------------
rows = st.slider("Number of rows", 1000, 20000, 5000, step=1000)

# -----------------------------
# Run pipeline
# -----------------------------
with st.spinner("Loading data..."):
    df = load_data(rows)

with st.spinner("Computing statistics..."):
    stats = compute_stats(df)

st.success("Done!")

# -----------------------------
# Display results
# -----------------------------
st.subheader("Sample Data")
st.dataframe(df.head())

st.subheader("Statistics")
st.dataframe(stats)

# -----------------------------
# NEW: Visualization
# -----------------------------
st.subheader("Value Distribution (Histogram)")
st.bar_chart(df["value"])
