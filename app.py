import streamlit as st
import os
from resume_parser import extract_text_from_pdf, parse_resume_sections
from skill_extractor import extract_skills, extract_education, extract_experience
from job_matcher import match_resume_to_job, generate_improvement_suggestions
from utils import clean_text, validate_pdf, format_skills

# Set page configuration
st.set_page_config(
    page_title="GenAI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .score-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .skill-match {
        color: #28a745;
        font-weight: bold;
    }
    .skill-miss {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">📄 GenAI Resume Analyzer & Job Match System</div>', unsafe_allow_html=True)

    # Sidebar for inputs
    st.sidebar.header("📤 Input Section")

    # Resume upload
    uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=['pdf'])

    # Job description input
    job_description = st.sidebar.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the job description here..."
    )

    # Analyze button
    analyze_button = st.sidebar.button("🔍 Analyze Resume", type="primary")

    # Main content area
    if analyze_button:
        if uploaded_file is None:
            st.error("Please upload a resume PDF file.")
            return

        if not job_description.strip():
            st.error("Please enter a job description.")
            return

        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Validate PDF
        if not validate_pdf(temp_path):
            st.error("Please upload a valid PDF file.")
            os.remove(temp_path)
            return

        # Process resume
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_text_from_pdf(temp_path)
            if not resume_text:
                st.error("Could not extract text from the PDF. Please try a different file.")
                os.remove(temp_path)
                return

        # Clean up temp file
        os.remove(temp_path)

        # Extract information
        with st.spinner("Analyzing resume content..."):
            skills = extract_skills(resume_text)
            education = extract_education(resume_text)
            experience = extract_experience(resume_text)

        # Match with job
        with st.spinner("Matching with job description..."):
            match_result = match_resume_to_job(resume_text, job_description, skills)
            suggestions = generate_improvement_suggestions(match_result['missing_skills'], resume_text)

        # Display results
        display_results(skills, education, experience, match_result, suggestions)

    else:
        # Welcome message
        st.info("👋 Welcome! Upload your resume and enter a job description to get started with the analysis.")

def display_results(skills, education, experience, match_result, suggestions):
    """Display analysis results in organized sections."""

    # Resume Information Section
    st.markdown('<div class="section-header">📋 Extracted Resume Information</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🎯 Skills")
        if skills:
            st.write(format_skills(skills))
        else:
            st.write("No skills extracted.")

    with col2:
        st.subheader("🎓 Education")
        if education:
            for edu in education[:3]:  # Show top 3
                st.write(f"• {edu}")
        else:
            st.write("No education information found.")

    with col3:
        st.subheader("💼 Experience")
        if experience:
            for exp in experience[:3]:  # Show top 3
                st.write(f"• {exp}")
        else:
            st.write("No experience information found.")

    # Job Match Section
    st.markdown('<div class="section-header">🎯 Job Match Analysis</div>', unsafe_allow_html=True)

    # Match Score
    score = match_result['match_score']
    st.markdown(f"""
    <div class="score-card">
        <h3>Job Compatibility Score: {score}%</h3>
        <p>This score represents how well your resume matches the job requirements based on semantic similarity.</p>
    </div>
    """, unsafe_allow_html=True)

    # Skills Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matching Skills")
        matching = match_result['matching_skills']
        if matching:
            for skill in matching:
                st.markdown(f'<span class="skill-match">✓ {skill.title()}</span>', unsafe_allow_html=True)
        else:
            st.write("No matching skills found.")

    with col2:
        st.subheader("❌ Missing Skills")
        missing = match_result['missing_skills']
        if missing:
            for skill in missing:
                st.markdown(f'<span class="skill-miss">✗ {skill.title()}</span>', unsafe_allow_html=True)
        else:
            st.write("No missing skills identified.")

    # Improvement Suggestions
    st.markdown('<div class="section-header">💡 Improvement Suggestions</div>', unsafe_allow_html=True)

    if suggestions:
        for suggestion in suggestions:
            st.info(f"💡 {suggestion}")
    else:
        st.success("Your resume looks comprehensive! No major improvements suggested.")

if __name__ == "__main__":
    main()
