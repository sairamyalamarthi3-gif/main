import streamlit as st
from sklearn.metrics import accuracy_score
import numpy as np

st.title("Model Accuracy Monitoring")
##base line accuracy
baseline_accuracy = 0.90
##Simulated production data
y_true_prod = [1,0,1,1,0,1,0,1]
y_pred_prod = [1,0,1,1,0,1,0,0]
## Calculate production accuracy
prod_accuracy= accuracy_score(y_true_prod,y_pred_prod)

st.metric("Baseline Accuracy",baseline_accuracy)
st.metric("Production Accuracy",prod_accuracy)

threshold = 0.02

if prod_accuracy < baseline_accuracy - threshold:
    st.error("Model accuracy dropped in production")
else:
    st.success("Model accuracy is stable")



