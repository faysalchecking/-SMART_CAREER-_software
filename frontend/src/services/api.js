import axios from 'axios'

const API_BASE_URL = import.meta.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Authentication endpoints
export const authAPI = {
  login: (email, password) =>
    apiClient.post('/auth/login/', { email, password }),
  logout: () =>
    apiClient.post('/auth/logout/'),
  me: () =>
    apiClient.get('/auth/me/'),
  refreshToken: () =>
    apiClient.post('/auth/refresh/'),
}

// Candidates endpoints
export const candidatesAPI = {
  list: (params) =>
    apiClient.get('/candidates/', { params }),
  get: (id) =>
    apiClient.get(`/candidates/${id}/`),
  create: (data) =>
    apiClient.post('/candidates/', data),
  update: (id, data) =>
    apiClient.patch(`/candidates/${id}/`, data),
  delete: (id) =>
    apiClient.delete(`/candidates/${id}/`),
}

// Jobs endpoints
export const jobsAPI = {
  list: (params) =>
    apiClient.get('/jobs/', { params }),
  get: (id) =>
    apiClient.get(`/jobs/${id}/`),
  create: (data) =>
    apiClient.post('/jobs/', data),
  update: (id, data) =>
    apiClient.patch(`/jobs/${id}/`, data),
}

export default apiClient