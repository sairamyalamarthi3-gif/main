import streamlit as st
import numpy as np
import pandas as pd
st.title(" Missing Values Monitoring")

##Simulated Production data

data = {
  "hours_studied": [5,None,6,4,None,7],
  "Attendance": [0.8,0,7,None,0.3,0.9],
}
df = pd.DataFrame(data)
st.subheader("Production Data Sample")
st.write(df)
##Calculate  missing values
missing_counts = df.isnull().sum()
st.subheader("Missing Value Count per Feature")
st.write(missing_counts)
# Alert logic
if missing_counts.sum() > 0:
    st.error("🚨 Missing values detected in production data!")
else:
    st.success("✅ No missing values detected")
