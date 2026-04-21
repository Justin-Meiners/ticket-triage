from fastapi import APIRouter
from pydantic import BaseModel
from services.classifier import classify_ticket

router = APIRouter()


class TriageRequest(BaseModel):
    text: str


class TriageResponse(BaseModel):
    urgency: str
    category: str
    tags: list[str]
    team: str
    routing_reason: str
    confidence: float
    ai_used: bool
    summary: str


@router.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    result = await classify_ticket(req.text)
    return {
        "urgency": result["urgency"],
        "category": result["category"],
        "tags": [result["category"]],
        "team": result["routing"],
        "routing_reason": result.get("routing_reason", ""),
        "confidence": result["confidence"],
        "ai_used": result["ai_used"],
        "summary": result.get("summary", ""),
    }
