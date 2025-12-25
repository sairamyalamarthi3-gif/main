import streamlit as st
st.title("Multi User Login")
##Define demo user
users = {
  "admin":"1234",
  "user1":"abcd",
  "user2":"pass"
}
##Session_state for Login
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
