import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const claimAPI = {
  uploadClaim: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/claims/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  getClaim: (claimId) => {
    return apiClient.get(`/claims/${claimId}`)
  },

  listClaims: () => {
    return apiClient.get('/claims')
  },

  getPendingClaims: () => {
    return apiClient.get('/claims/pending')
  },

  approveClaim: (claimId, notes) => {
    return apiClient.post(`/claims/${claimId}/approve`, {
      decision: 'approved',
      notes: notes
    })
  },

  denyClaim: (claimId, reason) => {
    return apiClient.post(`/claims/${claimId}/deny`, {
      decision: 'denied',
      denial_reason: reason
    })
  },

  deleteClaim: (claimId) => {
    return apiClient.delete(`/claims/${claimId}`)
  },

  getAuditLogs: () => {
    return apiClient.get('/audit-logs')
  },

  healthCheck: () => {
    return apiClient.get('/health')
  }
}

export default apiClient
