from fastapi import APIRouter, UploadFile, File
from app.services.extractor import extract_text

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    extracted_text = extract_text(file.filename, content)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text
    }
