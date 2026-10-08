import React, { useEffect, useState } from 'react'
import { claimAPI } from '../services/api'
import '../styles/Dashboard.css'

export default function ClaimReviewDashboard() {
  const [allClaims, setAllClaims] = useState([])
  const [filteredClaims, setFilteredClaims] = useState([])
  const [selectedClaim, setSelectedClaim] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('pending')
  const [auditLogs, setAuditLogs] = useState([])
  const [view, setView] = useState('claims')

  useEffect(() => {
    loadAllClaims()
    loadAuditLogs()
  }, [])

  useEffect(() => {
    filterClaims(filter)
  }, [allClaims, filter])

  const loadAllClaims = async () => {
    try {
      setLoading(true)
      const response = await claimAPI.listClaims()
      setAllClaims(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load claims')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const loadAuditLogs = async () => {
    try {
      const response = await claimAPI.getAuditLogs()
      setAuditLogs(response.data)
    } catch (err) {
      console.error('Failed to load audit logs', err)
    }
  }

  const filterClaims = (filterType) => {
    let filtered = allClaims

    if (filterType === 'pending') {
      filtered = allClaims.filter(claim =>
        ['pending', 'extracted', 'validated', 'recommended', 'flagged'].includes(claim.status)
      )
    } else if (filterType === 'approved') {
      filtered = allClaims.filter(claim => claim.status === 'approved')
    } else if (filterType === 'denied') {
      filtered = allClaims.filter(claim => claim.status === 'denied')
    }

    setFilteredClaims(filtered)
    setSelectedClaim(null)
  }

  const handleApprove = async () => {
    if (!selectedClaim) return

    try {
      await claimAPI.approveClaim(selectedClaim.id, '')
      loadAllClaims()
      setSelectedClaim(null)
    } catch (err) {
      setError('Failed to approve claim')
    }
  }

  const handleDeny = async () => {
    if (!selectedClaim) return

    const reason = prompt('Enter denial reason:')
    if (!reason) return

    try {
      await claimAPI.denyClaim(selectedClaim.id, reason)
      loadAllClaims()
      setSelectedClaim(null)
    } catch (err) {
      setError('Failed to deny claim')
    }
  }

  const handleDelete = async () => {
    if (!selectedClaim) return

    const confirmDelete = window.confirm(`Delete claim ${selectedClaim.claim_number}? This action cannot be undone.`)
    if (!confirmDelete) return

    try {
      await claimAPI.deleteClaim(selectedClaim.id)
      loadAllClaims()
      setSelectedClaim(null)
    } catch (err) {
      setError('Failed to delete claim')
    }
  }

  if (loading) return <div className="loading">Loading claims...</div>

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Claims Dashboard</h2>
        <button onClick={loadAllClaims} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="view-tabs">
        <button
          className={`view-tab ${view === 'claims' ? 'active' : ''}`}
          onClick={() => setView('claims')}
        >
          📋 Claims
        </button>
        <button
          className={`view-tab ${view === 'audit' ? 'active' : ''}`}
          onClick={() => { setView('audit'); loadAuditLogs() }}
        >
          📜 Audit Log ({auditLogs.length})
        </button>
      </div>

      {view === 'claims' && (
        <>
      <div className="filter-buttons">
        <button
          className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          ⏳ Pending ({allClaims.filter(c => ['pending', 'extracted', 'validated', 'recommended', 'flagged'].includes(c.status)).length})
        </button>
        <button
          className={`filter-btn ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => setFilter('approved')}
        >
          ✓ Approved ({allClaims.filter(c => c.status === 'approved').length})
        </button>
        <button
          className={`filter-btn ${filter === 'denied' ? 'active' : ''}`}
          onClick={() => setFilter('denied')}
        >
          ✗ Denied ({allClaims.filter(c => c.status === 'denied').length})
        </button>
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          📋 All ({allClaims.length})
        </button>
      </div>

      <div className="claims-grid">
        <div className="claims-list">
          <h3>{filter === 'all' ? 'All Claims' : filter === 'pending' ? 'Pending Claims' : filter === 'approved' ? 'Approved Claims' : 'Denied Claims'} ({filteredClaims.length})</h3>

          {filteredClaims.length === 0 ? (
            <div className="empty-state">No claims found</div>
          ) : (
            <ul>
              {filteredClaims.map(claim => (
                <li
                  key={claim.id}
                  className={`claim-item ${selectedClaim?.id === claim.id ? 'active' : ''}`}
                  onClick={() => setSelectedClaim(claim)}
                >
                  <div className="claim-header">
                    <strong>{claim.claim_number}</strong>
                    <span className={`status ${claim.status}`}>
                      {claim.status.toUpperCase()}
                    </span>
                  </div>
                  <div className="claim-summary">
                    <p>Amount: ${claim.extracted_data?.claim_amount || 'N/A'}</p>
                    <p>Patient: {claim.extracted_data?.patient_name || 'N/A'}</p>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {selectedClaim && (
          <div className="claim-details">
            <h3>Claim Details</h3>

            <div className="details-section">
              <h4>Extracted Information</h4>
              {selectedClaim.extracted_data && (
                <dl>
                  {Object.entries(selectedClaim.extracted_data).map(([key, value]) => (
                    <div key={key}>
                      <dt>{key}</dt>
                      <dd>{JSON.stringify(value)}</dd>
                    </div>
                  ))}
                </dl>
              )}
            </div>

            {selectedClaim.missing_fields?.length > 0 && (
              <div className="details-section warning">
                <h4>Missing Fields</h4>
                <ul>
                  {selectedClaim.missing_fields.map(field => (
                    <li key={field} className="missing-field">{field}</li>
                  ))}
                </ul>
              </div>
            )}

            {selectedClaim.recommendation && (
              <div className="details-section">
                <h4>AI Recommendation</h4>
                <div className={`recommendation ${selectedClaim.recommendation}`}>
                  <strong>{selectedClaim.recommendation?.toUpperCase()}</strong>
                  <p>Confidence: {(selectedClaim.recommendation_confidence * 100).toFixed(1)}%</p>
                  <p className="reason">{selectedClaim.recommendation_reason}</p>
                </div>
              </div>
            )}

            {['pending', 'extracted', 'validated', 'recommended', 'flagged'].includes(selectedClaim.status) && (
              <div className="action-buttons">
                <button onClick={handleApprove} className="approve-btn">
                  ✓ Approve
                </button>
                <button onClick={handleDeny} className="deny-btn">
                  ✗ Deny
                </button>
              </div>
            )}

            <div className="action-buttons">
              <button onClick={handleDelete} className="delete-btn">
                🗑️ Delete Claim
              </button>
            </div>
          </div>
        )}
      </div>
      </>
      )}

      {view === 'audit' && (
        <div className="audit-log-view">
          <h3>📜 Audit Log - All Actions</h3>
          {auditLogs.length === 0 ? (
            <div className="empty-state">No actions recorded</div>
          ) : (
            <table className="audit-table">
              <thead>
                <tr>
                  <th>Claim ID</th>
                  <th>Action</th>
                  <th>Actor</th>
                  <th>Details</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.map(log => (
                  <tr key={log.id}>
                    <td className="claim-id">{log.claim_id.substring(0, 8)}...</td>
                    <td>
                      <span className={`action-badge ${log.action.toLowerCase()}`}>
                        {log.action}
                      </span>
                    </td>
                    <td>{log.actor || 'System'}</td>
                    <td>{JSON.stringify(log.details)}</td>
                    <td className="timestamp">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
