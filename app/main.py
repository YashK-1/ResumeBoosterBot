# app/main.py
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import os

from .pdf_parser import extract_text_from_pdf
from .resume_analyzer import analyze_resume
from .together_llm import query_together
from .resume_utils import suggest_resume_boost 

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compute absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "templates"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "static"))

# Mount static files if directory exists
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Setup templates if directory exists
if os.path.isdir(TEMPLATE_DIR):
    templates = Jinja2Templates(directory=TEMPLATE_DIR)
else:
    templates = None

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Input Schema
class ResumeBoostRequest(BaseModel):
    resume_text: str
    job_title: str

# POST - Resume Boost via Hugging Face
@app.post("/boost-resume-upload/")
async def boost_resume_upload(resume_file: UploadFile = File(...), job_title: str = Form(...)):
    try:
        # Extract text from the uploaded PDF
        resume_text = await extract_text_from_pdf(resume_file)

        # Build prompt
        prompt = f"""
        You are a resume optimization assistant. Improve the following resume text for the job title '{job_title}'.

        Resume:
        {resume_text}

        Make it more impactful, highlight relevant skills, and make it ATS-friendly. Return the improved version.
        """

        # Query Hugging Face
        response = query_together(prompt)
        return {"boosted_resume": response}

    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "Not Found" in error_msg:
            return JSONResponse(
                status_code=502,
                content={"error": "TogetherAI API endpoint not found. Please check your model or endpoint configuration."}
            )
        return JSONResponse(status_code=500, content={"error": error_msg})