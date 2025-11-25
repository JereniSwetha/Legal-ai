import PyPDF2
from io import BytesIO

def extract_text(filename: str, file_bytes: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        extracted = ""
        for page in pdf_reader.pages:
            extracted += page.extract_text() or ""
        return extracted.strip()
    
    # For .txt or others
    try:
        return file_bytes.decode("utf-8")
    except:
        return file_bytes.decode("latin-1", errors="ignore")
