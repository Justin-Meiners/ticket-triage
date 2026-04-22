import { useEffect, useState } from "react";

const URGENCY_DOT = {
    critical: "#A32D2D",
    high:     "#854F0B",
    medium:   "#185FA5",
    low:      "#3B6D11",
};

export default function TicketHistory({ refreshKey, onSelect}) {
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function load() {
            setLoading(true);
            try {
                const res = await fetch("http://localhost:8000/api/tickets");
                const data = await res.json();
                setTickets(data);
            } catch {
                // Backend might not be ready, ignore errors
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [refreshKey]);

    async function handleDelete(e, id) {
        e.stopPropagation();
        await fetch (`http://localhost:8000/api/tickets/${id}`, { method: "DELETE" });
        setTickets((prev) => prev.filter((t) => t.id !== id));
    }

    
    return (
    <div className="card history-card">
      <h2 className="card-title">Recent tickets</h2>

      {loading && <p className="muted-text">Loading…</p>}

      {!loading && tickets.length === 0 && (
        <p className="muted-text">No tickets yet. Submit one to get started.</p>
      )}

      <ul className="history-list">
        {tickets.map((t) => (
          <li
            key={t.id}
            className="history-item"
            onClick={() => onSelect(t)}
          >
            <div className="history-item-header">
              <span
                className="urgency-dot"
                style={{ background: URGENCY_DOT[t.urgency?.toLowerCase()] ?? "#888" }}
              />
              <span className="history-urgency">{t.urgency}</span>
              <button
                className="delete-btn"
                onClick={(e) => handleDelete(e, t.id)}
                title="Delete"
              >
                ×
              </button>
            </div>
            <p className="history-snippet">
              {t.text?.slice(0, 90)}{t.text?.length > 90 ? "…" : ""}
            </p>
            <span className="history-date">{t.created_at}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
