import re
from nltk.tokenize import sent_tokenize
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

# Common technical skills database
COMMON_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
        'kotlin', 'golang', 'rust', 'typescript', 'scala', 'r', 'matlab'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data analysis', 'statistics', 'regression', 'classification',
        'clustering', 'neural networks'
    ],
    'frameworks': [
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'matplotlib', 'seaborn', 'plotly', 'react', 'angular', 'vue.js',
        'django', 'flask', 'fastapi', 'spring', 'hibernate'
    ],
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
        'dynamodb', 'elasticsearch', 'oracle'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'vercel'
    ],
    'devops': [
        'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
        'terraform', 'ansible', 'devops', 'ci/cd'
    ],
    'other_tools': [
        'git', 'linux', 'unix', 'windows', 'rest api', 'graphql',
        'microservices', 'agile', 'scrum', 'jira'
    ]
}

def extract_skills(text):
    """
    Extract skills from resume text using keyword matching.

    Args:
        text (str): Resume text.

    Returns:
        list: List of extracted skills.
    """
    skills = set()
    text_lower = text.lower()

    # Check against common skills database
    for category, skill_list in COMMON_SKILLS.items():
        for skill in skill_list:
            if skill in text_lower:
                skills.add(skill)

    # Remove duplicates and sort
    skills = sorted(list(skills))
    return skills

def extract_education(text):
    """
    Extract education information from resume text.

    Args:
        text (str): Resume text.

    Returns:
        list: List of education details found.
    """
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'certificate']

    education_details = []
    try:
        sentences = sent_tokenize(text)
    except:
        # Fallback: split by periods if tokenization fails
        sentences = [s.strip() for s in text.split('.') if s.strip()]

    for sentence in sentences:
        sentence_lower = sentence.lower()
        # Check if sentence contains education keywords
        if any(keyword in sentence_lower for keyword in education_keywords):
            education_details.append(sentence.strip())

    return education_details[:5]  # Return top 5

def extract_experience(text):
    """
    Extract work experience information from resume text.

    Args:
        text (str): Resume text.

    Returns:
        list: List of experience details found.
    """
    experience_keywords = ['worked', 'experience', 'responsibilities', 'led', 'managed', 'developed', 'implemented']

    experience_details = []
    try:
        sentences = sent_tokenize(text)
    except:
        # Fallback: split by periods if tokenization fails
        sentences = [s.strip() for s in text.split('.') if s.strip()]

    for sentence in sentences:
        sentence_lower = sentence.lower()
        # Check if sentence contains experience keywords
        if any(keyword in sentence_lower for keyword in experience_keywords):
            experience_details.append(sentence.strip())

    return experience_details[:5]  # Return top 5
