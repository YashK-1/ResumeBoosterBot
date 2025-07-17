from io import BytesIO
from PyPDF2 import PdfReader
from PyPDF2 import PdfReader
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    contents = await file.read()
    import io
    reader = PdfReader(io.BytesIO(contents))

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()