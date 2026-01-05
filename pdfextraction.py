import streamlit as st
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="PDF Text Extractor & Email Sender", layout="centered")

st.title("📄 PDF Text Extractor + Email Sender")

st.write("Upload a PDF, extract its text, and send it to your email.")

# -----------------------------
# Email sending function
# -----------------------------
def send_email(receiver_email, extracted_text):
    sender_email = "sairamyalamarthi3@gmail.com"
    sender_password = "wlwi bqle aehc aanh"  # Use App Password, not your real password

    # Email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Extracted PDF Text"

    message.attach(MIMEText(extracted_text, "plain"))

    # Send email via Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

# -----------------------------
# PDF Upload
# -----------------------------
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        st.subheader("📜 Extracted Text")
        st.text_area("Text Output", text, height=400)

        # Email input
        user_email = st.text_input("Enter your email to receive the extracted text")

        if st.button("Send Email"):
            if user_email.strip() == "":
                st.error("Please enter a valid email address.")
            else:
                try:
                    send_email(user_email, text)
                    st.success(f"Email sent successfully to {user_email}")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
