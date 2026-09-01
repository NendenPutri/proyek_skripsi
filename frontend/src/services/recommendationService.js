import { request } from './apiClient'

export function getRecommendations(payload) {
  return request('/api/recommendations', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
