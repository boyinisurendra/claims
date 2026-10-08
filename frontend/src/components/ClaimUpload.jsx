import React, { useState } from 'react'
import { claimAPI } from '../services/api'
import '../styles/ClaimUpload.css'

export default function ClaimUpload({ onSuccess }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError(null)
    } else {
      setError('Please select a valid PDF file')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first')
      return
    }

    setUploading(true)
    setProgress(0)

    try {
      setProgress(25)
      const response = await claimAPI.uploadClaim(file)
      setProgress(100)

      if (response.data) {
        setFile(null)
        setProgress(0)
        onSuccess(response.data)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="claim-upload">
      <div className="upload-container">
        <h2>Upload Claim PDF</h2>

        <div className="upload-area">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={uploading}
            className="file-input"
          />

          {file && (
            <div className="file-info">
              <p>📄 {file.name}</p>
              <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        {uploading && (
          <div className="progress-bar">
            <div className="progress" style={{ width: `${progress}%` }}></div>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-btn"
        >
          {uploading ? 'Processing...' : 'Upload & Process'}
        </button>
      </div>
    </div>
  )
}
