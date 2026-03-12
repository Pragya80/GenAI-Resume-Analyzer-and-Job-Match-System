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
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 2rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1f1f1f;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Score Card */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .score-card h3 {
        color: white;
        font-size: 1.2rem;
        margin: 0 0 1rem 0;
        opacity: 0.9;
    }
    
    .score-percentage {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        margin: 0.5rem 0;
    }
    
    .score-card p {
        color: rgba(255, 255, 255, 0.85);
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Skill Cards */
    .skill-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .skill-item {
        display: inline-block;
        background: white;
        padding: 0.7rem 1.2rem;
        border-radius: 25px;
        margin: 0.5rem 0.5rem 0.5rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .skill-match {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1f1f1f;
        font-weight: 600;
    }
    
    .skill-miss {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #1f1f1f;
        font-weight: 600;
    }
    
    /* Info Box */
    .info-box {
        background: #e7f3ff;
        border-left: 5px solid #2196F3;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        color: #0c5aa0;
    }
    
    .success-box {
        background: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        color: #2e7d32;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding: 2rem 1.5rem;
    }
    
    /* File Uploader */
    .stFileUploader {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Text Area */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Spinner Text */
    .stSpinner > div {
        color: #667eea;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">📄 GenAI Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">✨ Intelligent Resume Analysis & Job Matching System</div>', unsafe_allow_html=True)

    # Sidebar for inputs
    with st.sidebar:
        st.header("📤 Input Section")
        
        # Resume upload
        uploaded_file = st.file_uploader("📥 Upload Resume (PDF)", type=['pdf'])

        # Job description input
        job_description = st.text_area(
            "💼 Enter Job Description",
            height=200,
            placeholder="Paste the job description here...",
            label_visibility="visible"
        )

        # Analyze button
        analyze_button = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

    # Main content area
    if analyze_button:
        if uploaded_file is None:
            st.error("⚠️ Please upload a resume PDF file.")
            return

        if not job_description.strip():
            st.error("⚠️ Please enter a job description.")
            return

        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Validate PDF
        if not validate_pdf(temp_path):
            st.error("❌ Please upload a valid PDF file.")
            os.remove(temp_path)
            return

        # Process resume
        with st.spinner("🔄 Extracting text from resume..."):
            resume_text = extract_text_from_pdf(temp_path)
            if not resume_text:
                st.error("❌ Could not extract text from the PDF. Please try a different file.")
                os.remove(temp_path)
                return

        # Clean up temp file
        os.remove(temp_path)

        # Extract information
        with st.spinner("🔍 Analyzing resume content..."):
            skills = extract_skills(resume_text)
            education = extract_education(resume_text)
            experience = extract_experience(resume_text)

        # Match with job
        with st.spinner("⚙️ Matching with job description..."):
            match_result = match_resume_to_job(resume_text, job_description, skills)
            suggestions = generate_improvement_suggestions(match_result['missing_skills'], resume_text)

        # Display results
        display_results(skills, education, experience, match_result, suggestions)

    else:
        # Welcome message
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 2rem;">📊</div>
                <div class="metric-label">AI-Powered</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Advanced NLP Analysis</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 2rem;">⚡</div>
                <div class="metric-label">Instant Results</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Get Analysis in Seconds</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 2rem;">🎯</div>
                <div class="metric-label">Precise Matching</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Semantic Similarity</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        st.info("👋 **Welcome to GenAI Resume Analyzer!**\n\n"
                "1. **Upload** your resume in PDF format\n"
                "2. **Paste** the job description\n"
                "3. **Click Analyze** to get instant insights\n\n"
                "Get your job match score, skill analysis, and personalized improvement suggestions!")

def display_results(skills, education, experience, match_result, suggestions):
    """Display analysis results in organized sections."""

    # Resume Information Section
    st.markdown('<div class="section-header">📋 Extracted Resume Information</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem;">🎯</div>
            <div class="metric-label">Skills Found</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(skills)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem;">🎓</div>
            <div class="metric-label">Education</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(education)), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem;">💼</div>
            <div class="metric-label">Experience</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(experience)), unsafe_allow_html=True)

    # Detailed Information
    with st.expander("📚 View Detailed Information", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Skills Found")
            if skills:
                for skill in skills:
                    st.markdown(f"• **{skill.title()}**")
            else:
                st.write("No skills extracted.")

        with col2:
            st.subheader("🎓 Education")
            if education:
                for idx, edu in enumerate(education, 1):
                    st.write(f"{idx}. {edu[:80]}...")
            else:
                st.write("No education information found.")

        st.subheader("💼 Experience")
        if experience:
            for idx, exp in enumerate(experience, 1):
                st.write(f"{idx}. {exp[:100]}...")
        else:
            st.write("No experience information found.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Job Match Section
    st.markdown('<div class="section-header">🎯 Job Match Analysis</div>', unsafe_allow_html=True)

    # Match Score
    score = match_result['match_score']
    
    # Color coding based on score
    if score >= 80:
        gradient = "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)"
        description = "Excellent Match! 🌟"
    elif score >= 60:
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        description = "Good Match ✓"
    else:
        gradient = "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
        description = "Fair Match - Could Improve"
    
    st.markdown(f"""
    <div style="background: {gradient}; padding: 3rem; border-radius: 20px; text-align: center; color: white; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h3 style="color: white; margin: 0;">Job Compatibility Score</h3>
        <div style="font-size: 5rem; font-weight: 700; color: white; margin: 1rem 0;">{score}%</div>
        <p style="font-size: 1.2rem; margin: 0.5rem 0; color: rgba(255,255,255,0.9);">{description}</p>
        <p style="font-size: 0.95rem; color: rgba(255,255,255,0.8); margin-top: 1rem;">Based on semantic similarity between your resume and job description</p>
    </div>
    """, unsafe_allow_html=True)

    # Skills Analysis in Cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header" style="border-bottom: 3px solid #4caf50;">✅ Matching Skills</div>', unsafe_allow_html=True)
        matching = match_result['matching_skills']
        if matching:
            st.markdown('<div class="skill-container">', unsafe_allow_html=True)
            for skill in matching:
                st.markdown(f'<span class="skill-item skill-match">✓ {skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No matching skills found.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header" style="border-bottom: 3px solid #f44336;">❌ Missing Skills</div>', unsafe_allow_html=True)
        missing = match_result['missing_skills']
        if missing:
            st.markdown('<div class="skill-container">', unsafe_allow_html=True)
            for skill in missing:
                st.markdown(f'<span class="skill-item skill-miss">✗ {skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ No missing skills! You have all required skills.</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Improvement Suggestions
    st.markdown('<div class="section-header">💡 Improvement Suggestions</div>', unsafe_allow_html=True)

    if suggestions:
        for idx, suggestion in enumerate(suggestions, 1):
            st.markdown(f'<div class="info-box"><strong>💡 Suggestion {idx}:</strong> {suggestion}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">✅ <strong>Great Job!</strong> Your resume looks comprehensive. No major improvements suggested.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
