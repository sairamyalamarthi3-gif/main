import streamlit as st
import numpy as np
from sklearn.metrics import accuracy_score

st.title("Segement Wise Accuracy monitoring")

baseline_accuracy = 0.90
allowed_drop = 0.05

y_true = np.array([0,1,1,0,1,1,1,0,0,1,0,1,1])
y_pred = np.array([1,0,1,0,1,0,1,1,0,0,1,0,0])

# Segment info (0 = weekday, 1 = weekend)
day_type = np.array([0,0,0,0,1,1,1,1,0,0,1,1,0])

# Split by segment
weekday_idx = day_type == 0
weekend_idx = day_type == 1

weekday_acc = accuracy_score(y_true[weekday_idx], y_pred[weekday_idx])
weekend_acc = accuracy_score(y_true[weekend_idx], y_pred[weekend_idx])

# Display metrics
st.metric("Baseline Accuracy", baseline_accuracy)
st.metric("Weekday Accuracy", weekday_acc)
st.metric("Weekend Accuracy", weekend_acc)

# Alert logic
if weekday_acc < baseline_accuracy - allowed_drop:
    st.error("🚨 Accuracy drop detected for Weekday students")

if weekend_acc < baseline_accuracy - allowed_drop:
    st.error("🚨 Accuracy drop detected for Weekend students")

if (weekday_acc >= baseline_accuracy - allowed_drop and
    weekend_acc >= baseline_accuracy - allowed_drop):
    st.success("✅ Model performing well across all segments")
