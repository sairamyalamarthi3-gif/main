import streamlit as st
import PyPDF2

st.set_page_config(page_title="PDF Text Extractor", layout="centered")

st.title("📄 PDF Text Extractor")

st.write("Upload a PDF file and extract its text instantly.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        # Read PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        # Display extracted text
        st.subheader("📜 Extracted Text")
        st.text_area("Text Output", text, height=400)

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
