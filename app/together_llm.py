import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Load from .env OR Streamlit secrets
load_dotenv()
HF_API_KEY = st.secrets.get("HF_API_KEY", os.getenv("HF_API_KEY"))

HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def query_api_provider(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(HF_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Hugging Face API Error: {response.status_code} - {response.text}")

    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        content = result[0]["generated_text"]
    elif isinstance(result, dict) and "error" in result:
        raise Exception(f"❌ Hugging Face API Error: {result['error']}")
    else:
        raise Exception("❌ Unexpected Hugging Face API response format.")

    # Clean up and format
    formatted = content.strip().replace('\n\n', '\n').replace('\t', '')
    return formatted
