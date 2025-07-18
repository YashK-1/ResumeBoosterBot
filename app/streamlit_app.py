import streamlit as st
from tools import (
    extract_resume_text_tool,
    boost_resume_text_tool,
    generate_docx_tool,
    refine_resume_with_feedback_tool,
)

st.set_page_config(page_title="Resume Booster Bot", layout="wide")
st.title("🚀 Resume Booster Bot")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Job title input
job_title = st.text_input("Enter the job title you're targeting")

# Submit for improvement
if uploaded_file and job_title:
    with st.spinner("Extracting resume..."):
        resume_text = extract_resume_text_tool(uploaded_file)

    if "error" not in resume_text.lower():
        st.success("✅ Resume text extracted!")
        st.subheader("Original Resume Text")
        st.text_area("Original", resume_text, height=300)

        # Boost resume
        if st.button("✨ Boost Resume"):
            with st.spinner("Improving your resume..."):
                boosted_resume = boost_resume_text_tool(resume_text, job_title)

            if "error" not in boosted_resume.lower():
                st.success("✅ Resume boosted!")
                st.subheader("🔍 Improved Resume")
                st.text_area("Boosted", boosted_resume, height=300, key="boosted_output")

                # Feedback input
                st.subheader("✏️ Provide Feedback to Refine")
                feedback_input = st.text_input("What would you like to change or improve further?")

                if st.button("🔁 Apply Feedback"):
                    with st.spinner("Applying your feedback..."):
                        refined_resume = refine_resume_with_feedback_tool(boosted_resume, feedback_input)

                    if "error" not in refined_resume.lower():
                        st.success("✅ Resume refined with your feedback!")
                        st.text_area("Refined Resume", refined_resume, height=300, key="refined_output")
                        
                        # Download refined resume
                        docx_path = generate_docx_tool(refined_resume)
                        with open(docx_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Download Refined Resume (.docx)",
                                data=file,
                                file_name="Refined_Resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    else:
                        st.error(refined_resume)
                else:
                    # Download improved resume without feedback
                    docx_path = generate_docx_tool(boosted_resume)
                    with open(docx_path, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Boosted Resume (.docx)",
                            data=file,
                            file_name="Boosted_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
            else:
                st.error(boosted_resume)
    else:
        st.error(resume_text)
