const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000'

function normalizeBaseUrl(value) {
  const baseUrl = value?.trim() || DEFAULT_API_BASE_URL

  return baseUrl.replace(/\/+$/, '').replace(/\/api$/i, '')
}

function normalizeEndpoint(endpoint) {
  const value = String(endpoint || '')

  return value.startsWith('/') ? value : `/${value}`
}

export const API_BASE_URL = normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL)

export function buildApiUrl(endpoint) {
  return `${API_BASE_URL}${normalizeEndpoint(endpoint)}`
}
