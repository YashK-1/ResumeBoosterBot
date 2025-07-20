import streamlit as st
import asyncio
from tools import (
    extract_resume_text_tool,
    boost_resume_text_tool,
    generate_docx_tool,
    refine_resume_with_feedback_tool,
)

st.set_page_config(page_title="Resume Booster Bot", layout="wide")
st.title("🚀 Resume Booster Bot")

# --- Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_resume" not in st.session_state:
    st.session_state.current_resume = ""

if "job_title" not in st.session_state:
    st.session_state.job_title = ""

# --- Upload Resume ---
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_title_input = st.text_input("Enter the job title you're targeting")

if uploaded_file and job_title_input:
    st.session_state.job_title = job_title_input

    with st.spinner("Extracting resume..."):
        resume_text = extract_resume_text_tool(uploaded_file)
        if hasattr(resume_text, "__await__"):
            resume_text = asyncio.run(resume_text)

    if isinstance(resume_text, str) and "error" not in resume_text.lower():
        st.success("✅ Resume text extracted!")
        st.subheader("Original Resume Text")
        st.text_area("Original", resume_text, height=300)

        # --- Boost Resume ---
        if st.button("✨ Boost Resume"):
            with st.spinner("Improving your resume..."):
                boosted_resume = boost_resume_text_tool(resume_text, st.session_state.job_title)

            if "error" not in boosted_resume.lower():
                st.success("✅ Resume boosted!")
                st.subheader("🔍 Improved Resume")
                st.session_state.current_resume = boosted_resume
                st.text_area("Boosted", boosted_resume, height=300, key="boosted_output")

                # --- Download Button for Boosted Resume ---
                docx_path = generate_docx_tool(boosted_resume)
                with open(docx_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Boosted Resume (.docx)",
                        data=file,
                        file_name="Boosted_Resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                # --- Divider & Chat UI ---
                st.divider()
                st.subheader("💬 Refine Resume via Chat Feedback")

                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                feedback = st.chat_input("Give feedback or ask to change a section (e.g., 'Improve my summary')")

                if feedback:
                    st.chat_message("user").markdown(feedback)
                    st.session_state.messages.append({"role": "user", "content": feedback})

                    # Basic clarification for vague feedback
                    clarification_needed = any(x in feedback.lower() for x in ["improve", "change", "edit", "modify"]) and "summary" not in feedback.lower() and "experience" not in feedback.lower() and "skills" not in feedback.lower()

                    if clarification_needed:
                        clarification_msg = "🤖 Could you clarify which section you'd like to improve? (e.g., summary, skills, experience)"
                        st.chat_message("assistant").markdown(clarification_msg)
                        st.session_state.messages.append({"role": "assistant", "content": clarification_msg})
                    else:
                        # Refine resume
                        with st.spinner("Refining your resume..."):
                            improved = refine_resume_with_feedback_tool(st.session_state.current_resume, feedback)

                        st.session_state.current_resume = improved
                        st.chat_message("assistant").markdown(improved)
                        st.session_state.messages.append({"role": "assistant", "content": improved})

                        # --- Download Updated Resume ---
                        docx_path = generate_docx_tool(improved)
                        with open(docx_path, "rb") as f:
                            st.download_button(
                                label="📄 Download Refined Resume (.docx)",
                                data=f,
                                file_name="refined_resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
            else:
                st.error(boosted_resume)
    else:
        st.error(str(resume_text))
