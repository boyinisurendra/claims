import { useState } from 'react'
import ClaimUpload from './components/ClaimUpload'
import ClaimReviewDashboard from './components/ClaimReviewDashboard'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [successMessage, setSuccessMessage] = useState(null)

  const handleUploadSuccess = (claim) => {
    setSuccessMessage(`Claim ${claim.claim_number} processed successfully!`)
    setActiveTab('dashboard')

    setTimeout(() => setSuccessMessage(null), 5000)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏥 Insurance Claim Review Assistant</h1>
        <p>AI-powered claim processing and approval system</p>
      </header>

      {successMessage && (
        <div className="success-banner">
          {successMessage}
        </div>
      )}

      <nav className="app-nav">
        <button
          className={`nav-btn ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload Claim
        </button>
        <button
          className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📋 Review Dashboard
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'upload' && (
          <ClaimUpload onSuccess={handleUploadSuccess} />
        )}

        {activeTab === 'dashboard' && (
          <ClaimReviewDashboard />
        )}
      </main>

      <footer className="app-footer">
        <p>Version 1.0.0 | Healthcare Insurance Claim Review Assistant</p>
      </footer>
    </div>
  )
}

export default App
