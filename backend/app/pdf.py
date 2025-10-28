
from io import BytesIO
from pdfminer.high_level import extract_text

def extract_text_from_pdf_bytes(data: bytes) -> str:
    bio = BytesIO(data)
    try:
        text = extract_text(bio) or ""
    except Exception as e:
        text = ""
    return text
