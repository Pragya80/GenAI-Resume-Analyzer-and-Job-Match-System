import os
import re

def clean_text(text):
    """
    Clean and preprocess text.

    Args:
        text (str): Input text.

    Returns:
        str: Cleaned text.
    """
    # Remove extra whitespaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def get_file_size(file_path):
    """
    Get the size of a file in MB.

    Args:
        file_path (str): Path to the file.

    Returns:
        float: File size in MB.
    """
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)

def validate_pdf(file_path):
    """
    Validate if the file is a PDF.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if PDF, False otherwise.
    """
    return file_path.lower().endswith('.pdf')

def format_skills(skills_list):
    """
    Format a list of skills into a readable string.

    Args:
        skills_list (list): List of skills.

    Returns:
        str: Formatted skills string.
    """
    if not skills_list:
        return "No skills extracted."
    return ', '.join(skills_list)
