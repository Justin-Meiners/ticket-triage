import { useState } from 'react'
import './App.css'
import TicketForm from './components/TicketForm'

function App() {
  const [loading, setLoading] = useState(false)

  // TODO: implement actual submission logic once backend is ready
  function handleSubmit(_ticketText) {
    setLoading(true)
    setLoading(false)
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
        </div>
      </main>
    </div>
  )
}

export default App
