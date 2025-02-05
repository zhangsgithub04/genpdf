import streamlit as st
from fpdf2 import FPDF
import io
from google.generativeai import text

# Set your Gemini API key (replace with your actual key)
text.configure(api_key="YOUR_GEMINI_API_KEY")  # VERY IMPORTANT!

def generate_discussion(topic):
    try:
        response = text.generate_text(
            model="gemini-pro",  # Or another suitable Gemini model
            prompt=f"Generate a discussion about: {topic}",
            temperature=0.7,  # Adjust as needed
            max_output_tokens=500  # Adjust as needed
        )
        return response.result
    except Exception as e:
        st.error(f"Error generating discussion: {e}")
        return None


def create_pdf(discussion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Predefined layout (example)
    title_font_size = 16
    heading_font_size = 14
    content_font_size = 12
    margin = 20

    pdf.set_font("Arial", size=title_font_size, style="B")  # Title
    pdf.cell(0, 10, txt="Discussion on the Topic", ln=1, align="C")
    pdf.ln(10)

    # Split the discussion into sections (you'll likely want more sophisticated logic)
    sections = discussion.split("\n\n")  # Split by double newlines (adjust if needed)

    for i, section in enumerate(sections):
        if section.strip(): # Check if the section is not empty
            if i == 0:  # First section is treated as a general overview
                pdf.set_font("Arial", size=heading_font_size, style="B")
                pdf.cell(0, 10, txt="General Overview:", ln=1)
                pdf.set_font("Arial", size=content_font_size)
                pdf.multi_cell(0, 10, txt=section)
                pdf.ln(10)
            else:  # Other sections are treated as different points in the discussion
                pdf.set_font("Arial", size=heading_font_size, style="B")
                pdf.cell(0, 10, txt=f"Point {i}:", ln=1)
                pdf.set_font("Arial", size=content_font_size)
                pdf.multi_cell(0, 10, txt=section)
                pdf.ln(10)


    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


st.title("Gemini-Powered PDF Generator")

topic_input = st.text_input("Enter a topic for discussion:")

if st.button("Generate PDF"):
    if topic_input:
        discussion = generate_discussion(topic_input)
        if discussion:
            pdf_buffer = create_pdf(discussion)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="discussion.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please enter a topic.")
