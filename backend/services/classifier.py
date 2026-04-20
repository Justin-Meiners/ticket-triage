import os
from openai import OpenAI

URGENCY_KEYWORDS = {
    "critical": ["down", "outage", "breach", "data loss", "critical", "emergency"],
    "high":     ["broken", "error", "failing", "urgent", "blocked"],
    "medium":   ["slow", "degraded", "intermittent", "warning"],
    "low":      ["question", "feature", "request", "how do i"],
}

CATEGORY_KEYWORDS = {
    "billing":     ["invoice", "charge", "payment", "subscription", "billing"],
    "auth":        ["login", "password", "access", "permission", "auth"],
    "performance": ["slow", "latency", "timeout", "hang"],
    "bug":         ["error", "broken", "crash", "fail", "exception"],
    "feature":     ["feature", "request", "add", "would be nice"],
}

ROUTING = {
    "billing":     "Billing Team",
    "auth":        "Security Team",
    "performance": "Infrastructure Team",
    "bug":         "Engineering Team",
    "feature":     "Product Team",
}

CONFIDENCE_THRESHOLD = 0.6


def rule_based_classify(text: str) -> dict | None:
    lower = text.lower()

    urgency = "low"
    urgency_hits = 0
    for level, keywords in URGENCY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in lower)
        if hits:
            urgency = level
            urgency_hits = hits
            break

    category = None
    category_hits = 0
    for cat, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in lower)
        if hits:
            category = cat
            category_hits = hits
            break

    if category is None:
        return None

    total_hits = urgency_hits + category_hits
    confidence = min(0.9, 0.4 + total_hits * 0.1)

    routing_reason = f"Matched keywords: urgency({urgency_hits}), category({category_hits})"

    return {
        "urgency": urgency,
        "category": category,
        "routing": ROUTING.get(category, "Engineering Team"),
        "routing_reason": routing_reason,
        "confidence": round(confidence, 2),
    }


async def classify_with_ai(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    import json
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": (
                    "Classify this support ticket. Reply with JSON only, no extra text.\n"
                    "Fields: urgency (critical/high/medium/low), category (billing/auth/performance/bug/feature), "
                    "routing (team name), routing_reason (explanation), summary (one sentence).\n\n"
                    f"Ticket: {text}"
                ),
            }
        ],
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    data = json.loads(content.strip())
    data["confidence"] = 0.9
    data["ai_used"] = True
    return data


async def classify_ticket(text: str) -> dict:
    result = rule_based_classify(text)

    if result is None or result["confidence"] < CONFIDENCE_THRESHOLD:
        ai_result = await classify_with_ai(text)
        ai_result.setdefault("summary", "Classified by AI.")
        return ai_result

    result["ai_used"] = False
    result["summary"] = "Classified by rule-based engine."
    return result
