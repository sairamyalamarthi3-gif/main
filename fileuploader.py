import streamlit as st
import pandas as pd

st.title("File Uploader")

st.write("Upload a CSV file to view its contents")

uploaded_file = st.file_uploader("Choose a file",type ="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully")

    st.dataframe(df)

    st.write("### File Info")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
else:
    st.info("Please upload a CSV file")

    