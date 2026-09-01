import { request } from './apiClient'

export async function getAdminDashboardStats() {
  const response = await request('/api/admin/dashboard/stats')

  return response.data
}
