import streamlit as st
import os
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import base64

# Set up your Vertex AI API key (get it from Streamlit secrets or environment variables)
API_KEY = st.secrets.API_KEY  # Best practice: store API keys securely
genai.configure(api_key=API_KEY)

def generate_text(outline, content):
    """Generates text using Gemini."""
    prompt = f"""
    Generate a well-structured document based on the following outline and content:

    Outline:
    {outline}

    Content:
    {content}
    """

    model = genai.GenerativeModel("gemini-1.5-flash-002")  # Or a suitable Gemini model
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating text: {e}")  # Display error in Streamlit
        return None

def generate_pdf(generated_text):
    """Generates a PDF from the generated text in memory."""
    buffer = io.BytesIO()  # Use in-memory buffer

    c = canvas.Canvas(buffer, pagesize=letter)  # Use buffer for canvas

    text = c.beginText(50, 750)
    for line in generated_text.splitlines():
        text.textLine(line)
    c.drawText(text)
    c.save()  # Save to the buffer

    buffer.seek(0)  # Reset buffer position
    return buffer

def create_download_link(buffer, filename):
    """Creates a download link for the PDF."""
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF</a>'

st.title("Gemini PDF Generator")

outline_input = st.text_area("Outline", height=200)
content_input = st.text_area("Content", height=200)

if st.button("Generate PDF"):
    if outline_input and content_input:
        generated_text = generate_text(outline_input, content_input)
        if generated_text:
            pdf_buffer = generate_pdf(generated_text)
            html = create_download_link(pdf_buffer, "generated_document.pdf")
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("Please enter both outline and content.")
