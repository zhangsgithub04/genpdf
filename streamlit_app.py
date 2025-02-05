import streamlit as st
from fpdf2 import FPDF  # Or fpdf, but fpdf2 is preferred
import base64
import io

report_text = st.text_area("Report Text", height=200)

export_as_pdf = st.button("Export Report")

def create_download_link(buffer, filename):  # Correct function
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}.pdf">Download PDF</a>'

if export_as_pdf:
    if report_text:
        pdf = FPDF()  # Or fpdf2
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.multi_cell(0, 10, txt=report_text)  # Use multi_cell for text wrapping

        buffer = io.BytesIO()  # In-memory buffer is KEY!
        pdf.output(buffer)  # Output to the buffer
        buffer.seek(0)      # Reset the buffer's position (important!)

        html = create_download_link(buffer, "report")  # Pass the buffer
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("Please enter some text")
