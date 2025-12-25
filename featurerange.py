import streamlit as st
import pandas as pd
st.title("Feature Range Validation")
feature_range = {
  "hpurs_studied":(0,10),
  "attendance":(0.0,1.0)
}
##production data
data = {
  "hours_studied":[5,1,12,7,6],
  "attendance":[0.2,0.5,0.7,0.8,1.0]
}
df = pd.DataFrame(data)

st.subheader("Production Data")
st.write(df)
st.subheader("Range Validation Results")
##Validate feature ranges
for feature,(min_val,mex_val) in feature_range.items():
  out_of_range = df[
  (df[feature] < min_val) | (df[feature] > max_val)
  ]
 if not out_of_range.empty:
   st.error(f"🚨 {feature} has values outside range {min_val}–{max_val}")
   st.write(out_of_range[[feature]])
    else:
        st.success(f"✅ {feature} values are within range")
