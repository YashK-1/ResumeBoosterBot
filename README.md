# 🚀 ResumeBoosterBot (Agentic AI Resume Optimizer)

**ResumeBoosterBot** is an intelligent, agent-powered resume enhancement app that uses **LLM-driven tools** to rewrite, refine, and generate downloadable `.docx` resumes tailored to specific job roles.

Built with **Streamlit**, this project showcases how Agentic AI and Tool-using LLMs can improve real-world applications like resume writing, with features like multi-turn dialogue, chat feedback loop, and resume document generation.

---

## 🧠 Key Features

- 📄 **PDF Resume Upload**  
  Upload your existing resume in PDF format.

- 🧠 **AI-Powered Resume Optimization**  
  Boosts your resume using LLMs by tailoring it to the job title you provide.

- 🔁 **Agentic Feedback Loop**  
  Engage in a **chat-like UI** to refine your resume further through iterative feedback.

- 💬 **Multi-turn Chat Interface**  
  Seamless, continuous conversation with the bot to make section-wise or style-based improvements.

- 📥 **Downloadable `.docx` Output**  
  Save the final resume as a clean, ATS-friendly Microsoft Word file.

---

## 🛠️ Tech Stack

| Layer | Tools / Libraries |
|------|-------------------|
| Frontend | `Streamlit` |
| LLM Provider | `Together.ai` or `Ollama` (can be swapped) |
| Core Logic | Python + Agentic Tools |
| File Handling | `tempfile`, `python-docx`, PDF parsing |
| Resume Editing | LLM-based prompt engineering with custom feedback adaptation |

---

## 🚀 How It Works

1. **Upload your resume (PDF)**  
2. **Enter job title** for tailoring  
3. **LLM boosts** the resume with job-focused improvements  
4. **Chat interface** allows iterative user feedback (e.g., "Add a summary", "Make tone more formal")  
5. **Each refinement** updates the resume in real-time  
6. **Download** your final `.docx` resume
