import streamlit as st
from tools import (
    extract_resume_text_tool,
    boost_resume_text_tool,
    generate_docx_tool,
    refine_resume_with_feedback_tool
)

st.set_page_config(page_title="AI Resume Booster", layout="centered")
st.title("🚀 AI Resume Booster")

# Step 1: Upload resume PDF
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

# Step 2: Enter job title
job_title = st.text_input("💼 Enter the job title you're targeting:")

# Initialize session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "boosted_resume" not in st.session_state:
    st.session_state.boosted_resume = ""

if uploaded_file and job_title:
    if st.button("🔍 Analyze and Boost Resume"):
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_resume_text_tool(uploaded_file)
            st.session_state.resume_text = resume_text

        with st.spinner("Enhancing resume using AI..."):
            improved_resume = boost_resume_text_tool(
                st.session_state.resume_text, job_title
            )
            st.session_state.boosted_resume = improved_resume

# Display extracted and improved resume
if st.session_state.boosted_resume:
    st.subheader("✅ Improved Resume")
    st.text_area("📄 Boosted Resume Content", st.session_state.boosted_resume, height=400)

    # Generate download link for .docx
    with st.spinner("Generating Word document..."):
        docx_path = generate_docx_tool(st.session_state.boosted_resume)
        if isinstance(docx_path, str) and docx_path.endswith(".docx"):
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Improved Resume (.docx)",
                    data=f,
                    file_name="Improved_Resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
        else:
            st.error("⚠️ Failed to generate downloadable DOCX.")

st.subheader("🔄 Want to improve this further?")
user_feedback = st.text_input("Describe what you'd like to change or improve:")

if user_feedback:
    if st.button("Refine Resume"):
        with st.spinner("Refining your resume based on feedback..."):
            refined_resume = refine_resume_with_feedback_tool(resume_text, user_feedback)
            st.session_state["resume_text"] = refined_resume  # Optional: update session
            st.success("Here is your refined resume:")
            st.text_area("Refined Resume", refined_resume, height=600)
