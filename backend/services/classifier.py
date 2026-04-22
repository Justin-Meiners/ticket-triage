import os
import json
from openai import OpenAI

URGENCY_KEYWORDS = {
    "critical": {
        "weight": 4,
        "terms": [
            "outage", "down", "data loss", "breach", "security incident",
            "production down", "critical", "emergency", "corrupted", "deleted all",
        ],
    },
    "high": {
        "weight": 2,
        "terms": [
            "urgent", "asap", "immediately", "locked out", "broken", "not working",
            "demo", "deadline", "can't access", "cannot access", "blocked",
            "missing data", "wrong charge",
        ],
    },
    "medium": {
        "weight": 1,
        "terms": [
            "slow", "error", "issue", "problem", "bug", "incorrect", "missing",
            "not loading", "fails", "keeps crashing",
        ],
    },
    "low": {
        "weight": 1,
        "terms": [
            "feature request", "suggestion", "would love", "when will",
            "question", "wondering", "dark mode", "minor",
        ],
    },
}

CATEGORY_KEYWORDS = {
    "billing": [
        "charge", "charged", "payment", "invoice", "refund", "subscription",
        "billed", "credit card", "overcharge", "double charge", "receipt",
    ],
    "authentication": [
        "login", "log in", "password", "sign in", "locked out", "reset",
        "access", "2fa", "two-factor", "sso", "oauth",
    ],
    "performance": [
        "slow", "loading", "timeout", "lag", "latency", "speed",
        "performance", "unresponsive", "takes forever",
    ],
    "data & reporting": [
        "report", "missing", "disappeared", "deleted", "data", "export",
        "import", "lost", "not showing", "empty",
    ],
    "feature request": [
        "feature", "add", "would love", "suggestion", "request",
        "improve", "enhancement", "dark mode", "wish",
    ],
    "integrations & api": [
        "api", "integration", "webhook", "connect", "sync",
        "third-party", "import", "export", "zapier", "rest",
    ],
    "account management": [
        "account", "profile", "settings", "team", "user", "plan",
        "upgrade", "downgrade", "cancel",
    ],
}

ROUTING = {
    "billing":             ("Billing & Payments", "Ticket involves a financial transaction or subscription."),
    "authentication":      ("Identity & Access",  "User cannot authenticate or is locked out."),
    "performance":         ("Infrastructure",  "Possible reliability or latency issue in the platform."),
    "data & reporting":    ("Data & Recovery", "Potential data integrity or loss — needs investigation."),
    "feature request":     ("Product", "Enhancement request — route to product backlog."),
    "integrations & api":  ("Platform & Integrations",  "Issue involves an external connection or API usage."),
    "account management":  ("Account Management",  "Account-level configuration or access management."),
}

CONFIDENCE_THRESHOLD = 0.6
HIGH_CONFIDENCE = 8 


def rule_based_classify(text: str) -> dict | None:
    lower = text.lower()

    urgency_scores = {}
    total_weight = 0
    for level, data in URGENCY_KEYWORDS.items():
        hits = sum(1 for kw in data["terms"] if kw in lower)
        score = hits * data["weight"]
        urgency_scores[level] = score
        total_weight += score

    urgency = "low" if total_weight == 0 else max(urgency_scores, key=urgency_scores.get)

    category = None
    best_category_hits = 0
    for cat, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in lower)
        if hits > best_category_hits:
            best_category_hits = hits
            category = cat

    if category is None:
        return None

    confidence = min((total_weight + best_category_hits) / HIGH_CONFIDENCE, 1.0)
    team, routing_summary = ROUTING.get(category, ("Engineering Team", ""))

    return {
        "urgency": urgency,
        "category": category,
        "routing": team,
        "routing_reason": routing_summary,
        "confidence": round(confidence, 2),
    }


async def classify_with_ai(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    categories = list(CATEGORY_KEYWORDS.keys())
    teams = [team for team, _ in ROUTING.values()]
    urgency_levels = list(URGENCY_KEYWORDS.keys())

    prompt = (
        "Classify this support ticket. Reply with JSON only, no extra text.\n\n"
        f"urgency must be one of: {urgency_levels}\n"
        f"category must be one of: {categories}\n"
        f"routing must be one of: {teams}\n\n"
        "Fields:\n"
        "  urgency (string from the urgency list above)\n"
        "  category (string from the category list above)\n"
        "  routing (team name from the routing list above)\n"
        "  routing_reason (one sentence explaining why this team was chosen)\n"
        "  summary (one sentence summarizing the ticket)\n"
        "  confidence (float 0.0-1.0: how confident you are — lower if the ticket is ambiguous or fits multiple categories)\n\n"
        f"Ticket: {text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    data = json.loads(content.strip())
    data["ai_used"] = True
    data["confidence"] = round(max(0.0, min(1.0, float(data.get("confidence", 0.7)))), 2)
    return data


URGENCY_RANK = {"critical": 3, "high": 2, "medium": 1, "low": 0}

async def classify_ticket(text: str) -> dict:
    result = rule_based_classify(text)

    if result is None or result["confidence"] < CONFIDENCE_THRESHOLD:
        ai_result = await classify_with_ai(text)
        ai_result.setdefault("summary", "Classified by AI.")
        # Use rule-based urgency if it's more sever than AI's prediction
        if result is not None:
            rb_rank = URGENCY_RANK.get(result["urgency"], 0)
            ai_rank = URGENCY_RANK.get(ai_result.get("urgency", "low"), 0)
            if rb_rank > ai_rank:
                ai_result["urgency"] = result["urgency"]
        return ai_result

    result["ai_used"] = False
    result["summary"] = "Classified by rule-based engine."
    return result
