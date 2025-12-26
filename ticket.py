import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🎫 Ticket Generation System")

# Initialize session state for tickets
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# Ticket creation form
st.subheader("Create a New Ticket")

name = st.text_input("Your Name")
issue = st.text_area("Describe your issue")
priority = st.selectbox("Priority", ["Low", "Medium", "High"])

if st.button("Create Ticket"):
    if name and issue:
        ticket_id = f"TKT-{len(st.session_state.tickets) + 1}"
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_ticket = {
            "Ticket ID": ticket_id,
            "Name": name,
            "Issue": issue,
            "Priority": priority,
            "Status": "Open",
            "Created At": created_time
        }

        st.session_state.tickets.append(new_ticket)
        st.success(f"Ticket {ticket_id} created successfully!")
    else:
        st.error("Please fill in all required fields.")

# Display tickets
st.subheader("All Tickets")

if st.session_state.tickets:
    tickets_df = pd.DataFrame(st.session_state.tickets)
    st.dataframe(tickets_df)
else:
    st.info("No tickets created yet.")
