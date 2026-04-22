from fastapi import APIRouter
from pydantic import BaseModel
from services.classifier import classify_ticket
from routers.db import save_ticket, fetch_ticket_by_id

router = APIRouter()


class TriageRequest(BaseModel):
    text: str
    save: bool = True


class TriageResponse(BaseModel):
    id: int | None
    urgency: str
    category: str
    tags: list[str]
    team: str
    routing_reason: str
    confidence: float
    ai_used: bool
    summary: str
    created_at: str | None


@router.post("/triage", response_model=TriageResponse)
async def triage(req: TriageRequest):
    result = await classify_ticket(req.text)
    response = {
        "id": None,
        "urgency": result["urgency"],
        "category": result["category"],
        "tags": [result["category"]],
        "team": result["routing"],
        "routing_reason": result.get("routing_reason", ""),
        "confidence": result["confidence"],
        "ai_used": result["ai_used"],
        "summary": result.get("summary", ""),
        "created_at": None,
    }
    if req.save:
        ticket_id = save_ticket(req.text, response)
        row = fetch_ticket_by_id(ticket_id)
        if row:
            response["id"] = row["id"]
            response["created_at"] = row["created_at"]
    return response
