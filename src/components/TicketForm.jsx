import { useState } from "react";

export default function TicketForm({ onSubmit, loading }) {
    const [ticketText, setTicketText] = useState("");
    
    function handleSubmit(e) {
        e.preventDefault();
        onSubmit(ticketText);
    }

    return (
        <div className="card">
            <h2 className="card-title">Enter Ticket Text</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="ticket-input"
                    value={ticketText}
                    onChange={(e) => setTicketText(e.target.value)}
                    placeholder="Describe the issue in detail..."
                    rows={6}
                />
                <button type="submit" className="submit-btn" disabled={loading || !ticketText.trim()}>
                    {loading ? "Classifying..." : "Triage Ticket"}
                </button>
            </form>
        </div>
    );
}