import streamlit as st
import numpy as np
st.title("Prediction Confidence Monitoring")
##baseline confidence from training
baseline_confidence = 0.85
allowed_drop = 0.10
##Simulated production prediction confidence
prod_confidence = np.array([0.72,0.70,0.78,0.75,0.73,0.70])
##average confidence
avg_confidence = prod_confidence.mean()
##Display metrics
st.metric("Baseline Confidence",baseline_confidence)
st.metric("Production Avg Confidence",round(avg_confidence,2))
##Alert Logic
if avg_confidence < baseline_confidence - allowed_drop:
    st.error("Model confidence dropped in Production")
else:
    st.success("Model confidence is Stable")
# Optional visualization
st.line_chart(prod_confidence)
st.pie_chart(prod_confidence)
  
