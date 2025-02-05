import streamlit as st
from fpdf2 import FPDF
import io

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text) # Use multi_cell for text wrapping
    buffer = io.BytesIO()  # In-memory buffer
    pdf.output(buffer)
    buffer.seek(0)       # Rewind the buffer! (Crucial)
    return buffer

st.title("Simple PDF Generator")

text_input = st.text_area("Enter your text here:", height=200)

if st.button("Generate PDF"):
    if text_input:
        pdf_buffer = create_pdf(text_input)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="generated_pdf.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please enter some text.")
