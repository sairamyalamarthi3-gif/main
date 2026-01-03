import streamlit as st
import time

st.title("Streamlit Caching – Step 5 (Resource Caching)")

# -----------------------------
# Cached Resource (NEW)
# -----------------------------
@st.cache_resource
def get_fake_connection():
    time.sleep(2)  # simulate slow setup
    return "Connected to FakeDB"

# -----------------------------
# Cached Data Function
# -----------------------------
@st.cache_data
def slow_square(x: int):
    time.sleep(3)
    return x * x

# Clear cache button
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.warning("Cache cleared!")

# User input
num = st.number_input("Enter a number", min_value=0, max_value=100, value=10)

# Use the cached resource
with st.spinner("Connecting to database..."):
    conn = get_fake_connection()

# Use the cached data function
with st.spinner("Computing square..."):
    squared = slow_square(num)

st.success("Done!")

st.write("Database Status:", conn)
st.write("Square:", squared)
