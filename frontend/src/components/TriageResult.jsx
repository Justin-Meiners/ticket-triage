

export default function TriageResult({ result }) {
    if (!result) return null;

    return (
        <div className="triage-result card">
            <h2 className="card-title">Triage Result</h2>
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