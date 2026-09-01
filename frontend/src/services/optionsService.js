import { request } from './apiClient'

export function getOptions() {
  return request('/api/options')
}
