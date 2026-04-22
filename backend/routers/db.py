import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "tickets.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                urgency TEXT NOT NULL,
                tags TEXT NOT NULL,
                team TEXT NOT NULL,
                routing_reason TEXT,
                confidence REAL NOT NULL,
                ai_used BOOLEAN NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_ticket(text: str, result: dict) -> int:
    with get_db_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO tickets (text, urgency, tags, team, routing_reason, confidence, ai_used, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            text,
            result["urgency"],
            json.dumps(result.get("tags", [])),
            result["team"],
            result.get("routing_reason", ""),
            result["confidence"],
            result["ai_used"],
            result.get("summary", ""),
        ))
        conn.commit()
        return cursor.lastrowid

def fetch_recent_tickets(limit=10):
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    
    results = []
    for row in rows:
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        d["used_ai"] = bool(d["ai_used"])
        results.append(d)
    return results

def fetch_ticket_by_id(ticket_id: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (ticket_id,)
        ).fetchone()
    
    if row is None:
        return None
    
    d = dict(row)
    d["tags"] = json.loads(d["tags"])
    d["used_ai"] = bool(d["ai_used"])
    return d