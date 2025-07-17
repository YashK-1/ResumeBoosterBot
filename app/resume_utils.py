# app/resume_utils.py
from .together_llm import query_together

def suggest_resume_boost(resume_text, job_title):
    prompt = f"""
    You are a resume optimization assistant. Improve the following resume for the job title '{job_title}'.

    Resume:
    {resume_text}

    Make it more impactful, highlight relevant skills, and make it ATS-friendly.
    """
    return query_together(prompt)
