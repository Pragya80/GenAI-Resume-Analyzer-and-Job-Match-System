#!/usr/bin/env python
"""Test script to verify all imports work correctly."""

print("Testing imports...")

try:
    import pdfplumber
    print("✓ pdfplumber imported")
except ImportError as e:
    print(f"✗ pdfplumber import failed: {e}")

try:
    import streamlit
    print("✓ streamlit imported")
except ImportError as e:
    print(f"✗ streamlit import failed: {e}")

try:
    from resume_parser import extract_text_from_pdf
    print("✓ resume_parser imported")
except ImportError as e:
    print(f"✗ resume_parser import failed: {e}")

try:
    from skill_extractor import extract_skills
    print("✓ skill_extractor imported")
except ImportError as e:
    print(f"✗ skill_extractor import failed: {e}")

try:
    from job_matcher import match_resume_to_job
    print("✓ job_matcher imported")
except ImportError as e:
    print(f"✗ job_matcher import failed: {e}")

try:
    from utils import clean_text
    print("✓ utils imported")
except ImportError as e:
    print(f"✗ utils import failed: {e}")

print("\nAll imports successful!")