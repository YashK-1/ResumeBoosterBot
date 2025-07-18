from together_llm import query_api_provider
from docx import Document 

# Do NOT name any file in your project 'docx.py' or 'exceptions.py' to avoid import conflicts with python-docx.

def suggest_resume_boost(resume_text, job_title):
    prompt = f"""
    You are a resume optimization assistant. Improve the following resume for the job title '{job_title}'.

    Resume:
    {resume_text}

    Make it more impactful, highlight relevant skills, and make it ATS-friendly.
    """
    return query_api_provider(prompt)

def write_resume_to_docx(content, output_path="boosted_resume.docx"):
    doc = Document()
    doc.add_heading('Optimized Resume', 0)

    for line in content.split('\n'):
        if line.strip() == "":
            continue
        elif line.endswith(':'):
            doc.add_heading(line, level=1)
        else:
            doc.add_paragraph(line)

    doc.save(output_path)
