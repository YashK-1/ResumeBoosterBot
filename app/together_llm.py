import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

TOGETHER_API_KEY = st.secrets.get("TOGETHER_API_KEY", os.getenv("TOGETHER_API_KEY"))
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def query_api_provider(prompt: str) -> str:
    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",  # or another model available via Together
        "messages": [
            {"role": "system", "content": "You are a professional resume optimization assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 1024,
    }

    response = requests.post(TOGETHER_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Together API Error: {response.status_code} - {response.text}")

    result = response.json()
    content = result["choices"][0]["message"]["content"]
    return content.strip()
