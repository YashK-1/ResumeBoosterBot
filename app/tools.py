from pdf_parser import extract_text_from_pdf
from together_llm import query_api_provider
from resume_utils import write_resume_to_docx
import tempfile

# Tool 1: Extract resume text from uploaded PDF file
def extract_resume_text_tool(uploaded_file):
    """
    Extracts raw text from the uploaded resume PDF.
    """
    try:
        contents = uploaded_file.read()
        extracted_text = extract_text_from_pdf(contents)
        return extracted_text
    except Exception as e:
        return f"❌ Error extracting text: {e}"

# Tool 2: Enhance the resume using the AI provider
def boost_resume_text_tool(resume_text: str, job_title: str):
    """
    Boosts the resume using AI by providing an optimized version based on job title.
    """
    prompt = f"""
You are a professional resume optimization assistant. Rewrite and improve the resume text provided below, tailoring it for the job title: "{job_title}".

Structure the response in clearly defined sections:
1. Full Name (use placeholder if not provided)
2. Professional Summary (2-3 impactful lines)
3. Key Skills (bullet points)
4. Work Experience (chronological, bullet format under each job)
5. Education
6. Certifications (if any)
7. Projects (optional if mentioned)
8. Tools & Technologies (optional if relevant)

Resume Guidelines:
- Keep language concise and professional.
- Use action verbs and quantifiable achievements where possible.
- Make the resume ATS-friendly (avoid fancy formatting, icons, or tables).
- Emphasize relevant skills and experience for the job title: "{job_title}".
- Fix grammar, spelling, and formatting.
- Remove redundancy or irrelevant info.
- Assume standard formatting unless otherwise specified.

Resume Text:
{resume_text}
"""

    try:
        improved_resume = query_api_provider(prompt)
        return improved_resume.strip()
    except Exception as e:
        return f"❌ Error from AI API: {e}"

# Tool 3: Generate .docx from improved resume
def generate_docx_tool(boosted_resume_text: str):
    """
    Converts the improved resume text to a downloadable .docx file.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            write_resume_to_docx(boosted_resume_text, tmp.name)
            return tmp.name  # Return path to the saved .docx file
    except Exception as e:
        return f"❌ Error generating DOCX: {e}"
