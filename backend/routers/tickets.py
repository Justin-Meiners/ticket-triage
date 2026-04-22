from fastapi import APIRouter, HTTPException
from routers.db import fetch_recent_tickets, fetch_ticket_by_id, get_db_connection

router = APIRouter()


@router.get("/tickets")
def list_tickets(limit: int = 50):
    return fetch_recent_tickets(limit=limit)


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    ticket = fetch_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


@router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
    return {"deleted": ticket_id}
