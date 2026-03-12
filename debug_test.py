from job_matcher import match_resume_to_job
from skill_extractor import extract_skills

resume = "Python, AWS, Docker experience"
job = "SDE"
skills = extract_skills(resume)
print('Resume skills:', skills)
print('Match for generic job:', match_resume_to_job(resume, job, skills))
job2 = "Looking for Python and Docker expertise"
print('Match for detailed job:', match_resume_to_job(resume, job2, skills))
