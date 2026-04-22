import { useState } from "react";

const PRESETS = [
  {
    label: "Billing issue",
    text: "Hi, I was charged twice for my subscription this month — two charges of $49.99 on the 3rd and the 5th. I need this resolved ASAP. Order ref: ORD-88234.",
  },
  {
    label: "Login broken",
    text: "I cannot log into my account at all. I've tried resetting my password three times and the reset email never arrives. My whole team is locked out and we have a client demo in 2 hours. Critical!",
  },
  {
    label: "Feature request",
    text: "Hey, just a suggestion — would love to see a dark mode option in the dashboard someday. No rush, just a thought!",
  },
  {
    label: "Data loss",
    text: "All of the reports I created last week have disappeared from my account. I had over 20 custom reports and now the section is completely empty. Our quarter-end review is tomorrow.",
  },
  {
    label: "Slow performance",
    text: "The app has been loading slowly for the past few days — pages take 8-10 seconds. Not a blocker but definitely affecting my team's productivity.",
  },
];

export default function TicketForm({ onSubmit, loading }) {
    const [ticketText, setTicketText] = useState("");
    const [activePreset, setActivePreset] = useState(null);

    function loadPreset(preset, index) {
        setTicketText(preset.text);
        setActivePreset(index);
    }
    
    function handleSubmit(e) {
        e.preventDefault();
        onSubmit(ticketText);
    }

    return (
        <div className="card">
            <h2 className="card-title">Enter Ticket Text</h2>

            <div className="preset-row">
                {PRESETS.map((p, i) => (
                    <button
                        key={i}
                        className={'preset-chip ${activePreset === i ? "active" : ""}'}
                        onClick={() => loadPreset(p, i)}
                        type="button"
                    >
                        {p.label}
                    </button>
                ))}
            </div>
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