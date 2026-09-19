import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('darukaa_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error: { response?: { data?: { detail?: string } }; message?: string }) => {
    const detail = error.response?.data?.detail
    return Promise.reject(new Error(detail || error.message || 'Request failed.'))
  },
)
