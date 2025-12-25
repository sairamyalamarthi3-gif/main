import streamlit as st
import numpy as np
import pandas as pd
st.title("ML Ops Dashboard")
##Simulated Production Data
data = {
  "Hours_studied":[4,5,7,None,3],
  "Attendance":[0.1,0.5,0.6,None,1.3],
  "Prediction":[0,1,1,0,1],
  "Confidence":[0.81,0.65,0.43,0.90,0.53]
}
df = pd.DataFrame(data)
st.subheader("Simulted Production Data")
st.write(df)
##Missing Value Monitoring
st.subheader("Missing Value Monitoring")
missing_counts = df.isnull().sum()
st.write(missing_counts)
if missing_counts.sum() > 0:
  st.error("Missing Values Detected")
else:
  st.success(" No missing Values Detected")

##Feature Range Validation
st.subheader("Feature Range Validation")
feature_range = {
  "Hours_studied" : [0,10],
  "Attendance" : [0.0,1.0]
}
for feature,(min_val,max_val) in feature_range.items():
  out_of_range = df[
  (df[feature] < min_val) | (df[feature] > max_val)
  ]
  if not out_of_range.empty:
    st.error(f" {feature} out of range ({min_val}-{max_val})")
    st.write(out_of_range[[feature]])
  else:
    st.success(f"{feature} within range")

##Class Distribution monitoring
st.subheader("Class Distribution Monitoring")
pass_count = np.sum(df["Prediction"] == 1)
fail_count = np.sum(df["Prediction"] == 0)
st.metric("Pass Predictions", pass_count)
st.metric("Fail Predictions", fail_count)
dist_df = pd.DataFrame({
    "Class": ["Pass", "Fail"],
    "Count": [pass_count, fail_count]
}).set_index("Class")

st.bar_chart(dist_df)
###Confidence monitoring
st.subheader("📉 Prediction Confidence Monitoring")

baseline_confidence = 0.80
avg_confidence = df["confidence"].mean()

st.metric("Baseline Confidence", baseline_confidence)
st.metric("Production Avg Confidence", round(avg_confidence, 2))

if avg_confidence < baseline_confidence - 0.10:
    st.error("🚨 Model confidence dropped")
else:
    st.success("✅ Model confidence stable")
    
