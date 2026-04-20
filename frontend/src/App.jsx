import { useState } from 'react'
import './App.css'
import TicketForm from './components/TicketForm'
import TriageResult from './components/TriageResult'

function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(ticketText) {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: ticketText }),
      })
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-inner">
          <h1>Ticket Triage</h1>
          <p>Rule-based classification with AI overlay for ambiguous cases</p>
        </div>
      </header>
      <main className="app-main">
        <div className="left-col">
          <TicketForm onSubmit={handleSubmit} loading={loading} />
          {error && <p className="error-text">{error}</p>}
          <TriageResult result={result} />
        </div>
      </main>
    </div>
  )
}

export default App
