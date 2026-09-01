import { request } from './apiClient'

export function getHealth() {
  return request('/api/health')
}
