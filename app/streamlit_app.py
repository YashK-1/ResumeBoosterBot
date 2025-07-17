import streamlit as st
from together_llm import query_together
from PyPDF2 import PdfReader

# Page settings
st.set_page_config(page_title="Resume Booster Bot", layout="wide")

st.title("🚀 Resume Booster Bot")
st.markdown("Upload your resume and get an AI-optimized version tailored to a job title.")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_title = st.text_input("Enter Job Title")

if uploaded_file and job_title:
    # Extract text
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    if st.button("Boost Resume"):
        with st.spinner("Enhancing your resume with Together.ai..."):
            prompt = f"""
            You are a resume optimization assistant. Improve the following resume text for the job title '{job_title}'.
            Make it more impactful, highlight relevant skills, and make it ATS-friendly.

            Resume:
            {resume_text}
            """
            try:
                boosted = query_together(prompt)
                st.subheader("🔍 Optimized Resume")
                st.markdown(boosted.replace('\n', '  \n'))  # For line breaks in markdown
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
