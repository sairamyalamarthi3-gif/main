import streamlit as st
import numpy as np
st.title("Data Drift Monitoring")
# Training (baseline) feature
train_hours = np.array([1,2,3,4,5,6,7,8])

# Production feature
prod_hours = np.array([0.5,1,1.5,2,2,3,3])
# Compute statistics
train_mean = train_hours.mean()
prod_mean = prod_hours.mean()
st.metric("Training Mean (Hours Studied)", round(train_mean, 2))
st.metric("Production Mean (Hours Studied)", round(prod_mean, 2))

# Drift threshold
drift_threshold = 1.0

# Drift detection
if abs(train_mean - prod_mean) > drift_threshold:
    st.error("🚨 Data drift detected in input feature!")
else:
    st.success("✅ No significant data drift detected")

