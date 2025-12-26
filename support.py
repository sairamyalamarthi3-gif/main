import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🎧 Customer Support Queue")

# ---------- SESSION STATE ----------
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# ---------- CREATE TICKET ----------
with st.form("create_ticket"):
    st.subheader("📩 Create Support Ticket")
    customer = st.text_input("Customer Name")
    issue = st.text_input("Issue Description")
    submit_ticket = st.form_submit_button("Create Ticket")

if submit_ticket and customer and issue:
    st.session_state.tickets.append({
        "Customer": customer,
        "Issue": issue,
        "Status": "Open",
        "Created Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success("Ticket created")

# ---------- DISPLAY QUEUE ----------
if st.session_state.tickets:
    df = pd.DataFrame(st.session_state.tickets)

    st.subheader("📋 Ticket Queue")
    st.dataframe(df, use_container_width=True)

    # Ticket metrics
    open_tickets = df[df["Status"] == "Open"].shape[0]
    closed_tickets = df[df["Status"] == "Resolved"].shape[0]

    col1, col2 = st.columns(2)
    col1.metric("Open Tickets", open_tickets)
    col2.metric("Resolved Tickets", closed_tickets)

    # Resolve ticket
    st.subheader("✅ Resolve Ticket")
    open_customers = df[df["Status"] == "Open"]["Customer"].tolist()

    if open_customers:
        selected = st.selectbox("Select customer", open_customers)
        if st.button("Resolve"):
            for ticket in st.session_state.tickets:
                if ticket["Customer"] == selected and ticket["Status"] == "Open":
                    ticket["Status"] = "Resolved"
                    break
            st.success("Ticket resolved")
    else:
        st.info("No open tickets")

else:
    st.info("No tickets in queue yet")
