import streamlit as st
import numpy as np
import pandas as pd

st.title("Class Distribution Monitoring")
##Simulated Production Prediction
##1-Pass, 0- Fail
y_pred = np.array([1,0,1,0,0,1,0,1,1,0,1,0])
##Count_classes
pass_count = np.sum (y_pred == 1)
fail_count = np.sum (y_pred == 0)

##Show metrics

st.metrics("Pass Prediction",pass_count)
st.metrics("Fail Prediction",fail_count)

##Logic
total = pass_count + fail_count
pass_ratio = total/pass_count

if pass_ratio > 0.9 or pass_ratio < 0.1:
  st.error("Abnormal Distribution Detected")
else:
  st.success("Class distribution looks healthy")
  
