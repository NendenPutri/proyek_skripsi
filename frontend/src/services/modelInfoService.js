import { request } from './apiClient'

export function getModelInfo() {
  return request('/api/model-info')
}
