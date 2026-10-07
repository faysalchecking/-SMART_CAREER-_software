import apiClient from './api'

export const jobsAPI = {
  // List jobs with filters
  list: (params = {}) =>
    apiClient.get('/jobs/', { params }),

  // Get single job
  get: (id) =>
    apiClient.get(`/jobs/${id}/`),

  // Create job
  create: (data) =>
    apiClient.post('/jobs/', data),

  // Update job
  update: (id, data) =>
    apiClient.patch(`/jobs/${id}/`, data),

  // Delete job
  delete: (id) =>
    apiClient.delete(`/jobs/${id}/`),

  // Get available jobs
  available: () =>
    apiClient.get('/jobs/available/'),

  // Close job
  close: (id) =>
    apiClient.post(`/jobs/${id}/close/`),

  // Reopen job
  reopen: (id) =>
    apiClient.post(`/jobs/${id}/reopen/`),
}

export default jobsAPI