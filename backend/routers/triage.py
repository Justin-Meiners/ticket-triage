from fastapi import APIRouter
from pydantic import BaseModel
from services.classifier import classify_ticket

router = APIRouter()


class TriageRequest(BaseModel):
    text: str


class TriageResponse(BaseModel):
    urgency: str
    category: str
    routing: str
    confidence: float
    ai_used: bool
    summary: str


@router.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    result = await classify_ticket(req.text)
    return result
