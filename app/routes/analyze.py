from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_client import analyze_text

router = APIRouter(prefix="/analyze-basic", tags=["Analysis"])

class AnalyzeRequest(BaseModel):
    text: str

@router.post("/")
async def analyze_basic(req: AnalyzeRequest):
    response = analyze_text(req.text)
    return {"analysis": response}
