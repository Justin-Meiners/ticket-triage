const URGENCY_STYLES = {
  critical: { className: "badge badge-critical", label: "▲ Critical" },
  high:     { className: "badge badge-high",     label: "▲ High"     },
  medium:   { className: "badge badge-medium",   label: "● Medium"   },
  low:      { className: "badge badge-low",      label: "▼ Low"      },
};

function UrgencyBadge({ urgency }) {
  const key    = urgency?.toLowerCase() ?? "medium";
  const config = URGENCY_STYLES[key] ?? URGENCY_STYLES.medium;
  return <span className={config.className}>{config.label}</span>;
}
function ConfidenceBar({ confidence, usedAI }) {
    const pct = Math.round(confidence * 100);
    const label = usedAI ? `AI Overlay ${pct}%` : `Rule-Based ${pct}%`;
    return (
        <div className="confidence-wrap">
            <div className="confidence-bar-bg">
                <div className="confidence-bar-fill"
                style={{ width: `${pct}%` }}/>
            </div>
            <span className="confidence-label">{label}</span>
        </div>
    )
}

export default function TriageResult({ result }) {
    if (!result) return null;
    return (
        <div className="triage-result card">
            <h2 className="card-title">Triage Result</h2>
            <ConfidenceBar confidence={result.confidence} usedAI={result.ai_used} />
            <div className="result-row">
                <span className="result-label">Urgency</span>
                <UrgencyBadge urgency={result.urgency} />
            </div>
            <div className="result-row">
                <span className="result-label">Categories</span>
                <div className="tag-list">
                    {(result.tags ?? []).map((category) => (
                        <span key={category} className="tag">
                            {category}
                        </span>
                    ))}
                </div>
            </div>

            <div className="result-row routing-row">
                <span className="result-label">Route To</span>
                <div className="routing-card">
                    <div>
                        <div className="routing-team">{result.team}</div>
                        <div className="routing-reason">{result.routing_reason}</div>
                    </div>
                </div>
            </div>

            {result.summary && (
                <div className="summary-block">
                    <h3 className="summary-label">Summary</h3>
                    <p className="summary-text">{result.summary}</p>
                </div>
            )}

            {result.id && (
                <div className="result-meta">Saved -- ticket #{result.id} -- {result.created_at}</div>
            )}
        </div>
    );
}