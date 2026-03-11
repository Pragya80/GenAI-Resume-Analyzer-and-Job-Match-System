import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfplumber.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

    # Clean the extracted text
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'\s+', ' ', text)   # Remove extra spaces
    return text.strip()

def parse_resume_sections(text):
    """
    Parse the resume text into sections like education, experience, skills.

    Args:
        text (str): Full text of the resume.

    Returns:
        dict: Dictionary with sections.
    """
    sections = {
        'education': '',
        'experience': '',
        'skills': '',
        'other': ''
    }

    # Simple regex-based section detection (can be improved)
    education_match = re.search(r'(?i)education[:\s]*(.*?)(?=\n[A-Z]|$)', text, re.DOTALL)
    if education_match:
        sections['education'] = education_match.group(1).strip()

    experience_match = re.search(r'(?i)experience[:\s]*(.*?)(?=\n[A-Z]|$)', text, re.DOTALL)
    if experience_match:
        sections['experience'] = experience_match.group(1).strip()

    skills_match = re.search(r'(?i)skills[:\s]*(.*?)(?=\n[A-Z]|$)', text, re.DOTALL)
    if skills_match:
        sections['skills'] = skills_match.group(1).strip()

    # The rest goes to other
    sections['other'] = text

    return sections
