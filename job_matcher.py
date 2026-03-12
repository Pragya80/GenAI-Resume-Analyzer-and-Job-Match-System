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
        dict: Dictionary with match score, matching skills, missing skills, and a flag
              indicating whether any skills were found in the job description.
    """
    # Calculate overall similarity
    overall_similarity = calculate_similarity(resume_text, job_description)
    match_score = round(overall_similarity * 100, 2)

    # Extract skills from job description
    job_skills = extract_job_skills(job_description)

    # Find matching and missing skills
    matching_skills = [skill for skill in resume_skills if skill in job_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    return {
        'match_score': match_score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'job_skills_found': bool(job_skills)
    }

def extract_job_skills(job_description):
    """
    Extract skills from a job description. Reuses the same keyword database as the
    resume extractor, ensuring consistency and better coverage.

    Args:
        job_description (str): Job description text.

    Returns:
        list: List of skills mentioned in job description.
    """
    # simple approach: leverage the resume skill extractor so we don't duplicate
    # the skill list.  this will catch any skill from COMMON_SKILLS that appears
    # in the description.
    from skill_extractor import extract_skills

    # running extract_skills on the job description text returns any of the
    # recognized skills.  the extractor already lowercases and does simple
    # substring matching.
    skills = extract_skills(job_description)

    # if nothing was found and the description is very short, the user likely
    # entered a generic title (e.g. "SDE").  we leave the list empty so the
    # calling code can display a warning.
    return skills

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
