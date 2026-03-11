from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(text1, text2):
    """
    Calculate cosine similarity between two texts using sentence embeddings.

    Args:
        text1 (str): First text.
        text2 (str): Second text.

    Returns:
        float: Similarity score between 0 and 1.
    """
    embeddings1 = model.encode([text1])
    embeddings2 = model.encode([text2])
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity

def match_resume_to_job(resume_text, job_description, resume_skills):
    """
    Match resume to job description and calculate compatibility score.

    Args:
        resume_text (str): Full resume text.
        job_description (str): Job description text.
        resume_skills (list): List of skills extracted from resume.

    Returns:
        dict: Dictionary with match score, matching skills, missing skills.
    """
    # Calculate overall similarity
    overall_similarity = calculate_similarity(resume_text, job_description)
    match_score = round(overall_similarity * 100, 2)

    # Extract skills from job description (simple keyword matching)
    job_skills = extract_job_skills(job_description)

    # Find matching and missing skills
    matching_skills = [skill for skill in resume_skills if skill in job_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    return {
        'match_score': match_score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills
    }

def extract_job_skills(job_description):
    """
    Extract skills from job description using simple keyword matching.

    Args:
        job_description (str): Job description text.

    Returns:
        list: List of skills mentioned in job description.
    """
    # This is a simplified version; in a real app, use more sophisticated NLP
    common_skills = [
        'python', 'java', 'javascript', 'sql', 'machine learning', 'data analysis',
        'nlp', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy',
        'scikit-learn', 'react', 'node.js', 'aws', 'docker', 'kubernetes'
    ]

    job_skills = []
    for skill in common_skills:
        if skill in job_description.lower():
            job_skills.append(skill)

    return job_skills

def generate_improvement_suggestions(missing_skills, resume_text):
    """
    Generate suggestions to improve the resume based on missing skills.

    Args:
        missing_skills (list): List of missing skills.
        resume_text (str): Resume text.

    Returns:
        list: List of improvement suggestions.
    """
    suggestions = []

    if missing_skills:
        suggestions.append(f"Consider adding or highlighting the following skills in your resume: {', '.join(missing_skills)}")

    # Check for sections
    if 'education' not in resume_text.lower():
        suggestions.append("Add an Education section to highlight your academic background.")

    if 'experience' not in resume_text.lower():
        suggestions.append("Add a Work Experience section to detail your professional background.")

    if len(resume_text.split()) < 200:
        suggestions.append("Your resume seems short. Consider adding more details about your projects and achievements.")

    return suggestions
