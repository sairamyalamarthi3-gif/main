import streamlit as st
import numpy as np
from sklearn.metrics import accuracy_score
st.title("Rolling Accuracy Monitoring")
baseline_accuracy = 0.90
allowed_drop = 0.05

# Simulated production data (streaming-like)
# 1 = pass, 0 = fail

y_true_prod = np.array([1,0,1,0,0,0,0,1,0,1])
y_pred_prod = np.array([1,1,0,0,1,0,0,1,0,1])

window_size = 5
recent_true = y_true_prod[-window_size:]
recent_pred = y_pred_prod[-window_size:]

# Compute rolling accuracy
rolling_accuracy = accuracy_score(recent_true,recent_pred)

##Display metrics
st.metric("Baseline Accuracy", baseline_accuracy)
st.metric("Rolling Production Accuracy", rolling_accuracy)

# Alert logic
if rolling_accuracy < baseline_accuracy - allowed_drop:
    st.error("🚨 Accuracy dropped in recent production window!")
else:
    st.success("✅ Model performing within acceptable range")

st.caption(f"Accuracy calculated on last {window_size} predictions")
