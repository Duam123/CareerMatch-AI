
import re

SKILLS = [
    "python", "java", "javascript", "typescript",
    "html", "css", "react", "node.js", "django",
    "flask", "fastapi", "php", "laravel",
    "sql", "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning", "generative ai",
    "langchain", "rag", "data analysis", "pandas",
    "numpy", "scikit-learn", "git", "rest api",
    "testing", "selenium", "postman", "communication",
    "problem solving", "project management"
]


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))


def match_resume(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if not job_skills:
        return {
            "score": 0,
            "resume_skills": resume_skills,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    score = round(len(matched) / len(job_skills) * 100, 1)

    return {
        "score": score,
        "resume_skills": resume_skills,
        "matched_skills": matched,
        "missing_skills": missing,
    }
