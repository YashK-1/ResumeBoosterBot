# app/resume_analyzer.py
from .pdf_parser import extract_text_from_pdf

def analyze_resume(file):
    resume_text = extract_text_from_pdf(file)
    return resume_text