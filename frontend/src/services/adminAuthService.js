import { request } from './apiClient'

export async function loginAdmin(payload) {
  const response = await request('/api/admin/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
    skipAuth: true,
  })

  return response.data
}

export async function getCurrentAdmin() {
  const response = await request('/api/admin/auth/me')

  return response.data
}

