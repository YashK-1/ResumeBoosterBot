import requests
import os
import streamlit as st
from dotenv import load_dotenv
"""from dotenv import load_dotenv
load_dotenv()
key = os.getenv("TOGETHER_API_KEY")"""
# TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
load_dotenv()

TOGETHER_API_KEY = st.secrets.get("TOGETHER_API_KEY", os.getenv("TOGETHER_API_KEY"))
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def query_together(prompt: str) -> str:
    payload = {
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "messages": [
            {"role": "system", "content": "You are a resume rewriting assistant. Improve resumes for ATS and recruiter clarity."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 1024,
    }

    response = requests.post(TOGETHER_API_URL, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"TogetherAI API Error: {response.status_code} - {response.text}")
    
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    
    # Clean up and format
    formatted = content.strip().replace('\n\n', '\n').replace('\t', '')
    return formatted

