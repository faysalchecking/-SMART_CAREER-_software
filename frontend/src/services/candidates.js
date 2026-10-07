import apiClient from './api'

export const candidatesAPI = {
  // List candidates with filters
  list: (params = {}) =>
    apiClient.get('/candidates/', { params }),

  // Get single candidate
  get: (id) =>
    apiClient.get(`/candidates/${id}/`),

  // Create candidate
  create: (data) =>
    apiClient.post('/candidates/', data),

  // Update candidate
  update: (id, data) =>
    apiClient.patch(`/candidates/${id}/`, data),

  // Delete candidate
  delete: (id) =>
    apiClient.delete(`/candidates/${id}/`),

  // Change candidate status
  changeStatus: (id, status) =>
    apiClient.post(`/candidates/${id}/change_status/`, { status }),

  // Get expiring passports
  expiringPassports: () =>
    apiClient.get('/candidates/expiring_passports/'),

  // Get expired passports
  expiredPassports: () =>
    apiClient.get('/candidates/expired_passports/'),
}

export default candidatesAPI