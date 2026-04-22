# Ticket Triage

A full-stack support ticket classification tool that combines a keyword-based rule engine with GPT-4o-mini to automatically cateogirze, prioritize, and route incoming tickets.

## Features

- Hybrid Classification - a rule-based engine handles clear-cut tickets instantly; ambiguous tickets are handled by a GPT API call

- Category & Routing - maps tickets to categories (billing, auth, performance, bug, feature) and suggests the responsible team

- Confidence scoring - shows how confident the classifier was and whether AI or the rule engine made the classification

- Ticket history - persists all triaged tickets in SQLite with timestamps; supports browsing and deletion

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | React 19, Vite                    |
| Backend  | FastAPI, Python 3.12+             |
| AI       | OpenAI GPT-4o-mini                |
| Database | SQLite (via Python's `sqlite3`)   |


## Guide

### Prerequisites

- Python 3.12+
- Node.js 18+
- An OpenAI API key

### Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create a .env file and place "OPENAI_API_KEY={key}"

uvicorn main:app --reload


### Frontend
cd frontend
npm install
npm run dev

## How Classification Works
- The rule engine scans the ticket text for keyword matches
- If the rule engine matches with confidence >= 0.6, it returns that result immediately
- Otherwise, the ticket is sent to GPT-4o-mini for classification
- If the rule engine flagged a higher urgency than the AI did, the rule-based urgency is used as an override