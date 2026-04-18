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


def rule_based_classify(text: str) -> dict:
    lower = text.lower()

    urgency = "low"
    for level, keywords in URGENCY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            urgency = level
            break

    category = "bug"
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            category = cat
            break

    word_count = len(text.split())
    confidence = min(0.9, 0.4 + word_count * 0.02)

    return {
        "urgency": urgency,
        "category": category,
        "routing": ROUTING.get(category, "Engineering Team"),
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
                    "routing (team name), summary (one sentence).\n\n"
                    f"Ticket: {text}"
                ),
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)
    data["confidence"] = 0.9
    data["ai_used"] = True
    return data


async def classify_ticket(text: str) -> dict:
    result = rule_based_classify(text)

    if result["confidence"] < CONFIDENCE_THRESHOLD:
        ai_result = await classify_with_ai(text)
        ai_result.setdefault("summary", "Classified by AI.")
        return ai_result

    result["ai_used"] = False
    result["summary"] = "Classified by rule-based engine."
    return result
