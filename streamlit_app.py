import streamlit as st
import os
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import base64

API_KEY = st.secrets["gemini_api_key"]  # Best practice: store API keys securely
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



default_lab_manual_outline="""
Here is a suggested outline for a lab manual for a specific class:
Lab Title
[Insert lab title, e.g., "Lab 3: Vulnerability Scanning and Management"]
Introduction
Briefly introduce the lab, including:
Learning objectives
Overview of the lab exercise
Importance of the lab topic
Prerequisites
List any prerequisites for the lab, including:
Required reading or assignments
Prior knowledge or skills
Software or hardware requirements
Procedures
Step-by-step instructions for completing the lab exercise, including:
Setup and configuration
Execution of the lab exercise
Troubleshooting tips
Results
Instructions for recording and analyzing results, including:
Data collection and measurement
Data analysis and interpretation
Expected outcomes and results
Summary
Brief summary of the lab exercise, including:
Key findings and takeaways
Implications and applications
Review questions or discussion topics
Additional Resources
Optional section for providing additional resources, including:
References and citations
Online resources and tutorials
Software or hardware documentation
Grading Criteria
Optional section for outlining grading criteria, including:
Lab report requirements
Evaluation criteria
Point values or weights

"""

outline_input = st.text_area("Outline", value=default_lab_manual_outline, height=200)
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
