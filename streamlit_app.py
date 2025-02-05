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
    Generate a well-structured document based on the following outline and content, using proper necessary formattings and multiple pages as needed, to feed into reportlab.

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

"""Creates a download link for the PDF."""
"""
def create_download_link(buffer, filename, type):
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF</a>'
"""
def create_download_link(buffer, filename, file_type):
    """Creates a download link for the file."""
    mime_types = {
        "pdf": "application/pdf",
        "tex": "application/x-latex",
        "txt": "text/plain",
        "csv": "text/csv",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    mime_type = mime_types.get(file_type, "application/octet-stream")  # Default if type is unknown.

    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {file_type.upper()}</a>'
    return href
    

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

default_lab_content = """
I'll provide a basic example of a buffer overflow vulnerability using C and the GCC compiler on a Linux system. Please note that intentionally exploiting vulnerabilities is not recommended and should only be done in a controlled environment.
Vulnerable Code
Create a file called vulnerable.c with the following code:
C
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[10];
    strcpy(buffer, input);
    printf("You entered: %s\n", buffer);
}

int main() {
    char input[100];
    printf("Enter your input: ");
    fgets(input, sizeof(input), stdin);
    vulnerable_function(input);
    return 0;
}
Compile the Vulnerable Code
Compile the code using the GCC compiler:
Bash
gcc -g -fno-stack-protector vulnerable.c -o vulnerable
Reproduce the Buffer Overflow
Use a tool like gdb or a Python script to send a large input to the vulnerable program:
Using GDB:
Bash
gdb ./vulnerable
(gdb) run
Enter your input: $(python -c 'print("A"*20)')
Using a Python Script:
Bash
python -c 'print("A"*100)' | ./vulnerable
Analyze the Crash
After running the vulnerable program with a large input, it should crash. You can analyze the crash using gdb:
Bash
gdb ./vulnerable core
(gdb) bt
This will display the backtrace of the crash, showing the overflowed buffer.
Please note that this is a simplified example and real-world buffer overflow vulnerabilities can be much more complex. Additionally, it's essential to follow proper security practices and guidelines when working with vulnerable code.
"""
outline_input = st.text_area("Outline", value=default_lab_manual_outline, height=200)
content_input = st.text_area("Content", value=default_lab_content, height=200)

if st.button("Generate PDF"):
    if outline_input and content_input:
        generated_text = generate_text(outline_input, content_input)
        if generated_text:
            # Display the generated text on the GUI for debugging
            st.write("## Generated Text (For Debugging):")  # Markdown heading
            st.write(generated_text)  # Display the text

            pdf_buffer = generate_pdf(generated_text)
            # ... (download link creation as before)
            html1 = create_download_link(pdf_buffer, "generated_lab_manual.pdf", "pdf")
            st.markdown(html1, unsafe_allow_html=True)
            html2 = create_download_link(pdf_buffer, "generated_lab_manual.tex", "tex")
            st.markdown(html2, unsafe_allow_html=True)
        else:
            st.error("Failed to generate text. Check the Gemini API.")  # More specific error message
    else:
        st.warning("Please enter both outline and content.")
        
