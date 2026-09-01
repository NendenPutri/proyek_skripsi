import { request } from './apiClient'

const adminLaptopQueryKeys = [
  'page',
  'limit',
  'search',
  'category',
  'status',
  'source',
  'sort_by',
  'sort_order',
]

function buildAdminLaptopQuery(params = {}) {
  const searchParams = new URLSearchParams()

  adminLaptopQueryKeys.forEach((key) => {
    const value = params[key]

    if (value !== undefined && value !== null && value !== '') {
      searchParams.set(key, value)
    }
  })

  const queryString = searchParams.toString()

  return queryString ? `?${queryString}` : ''
}

export async function getAdminLaptops(params = {}) {
  const response = await request(`/api/admin/laptops${buildAdminLaptopQuery(params)}`)

  return response.data
}

export async function getAdminLaptopById(laptopId) {
  const response = await request(`/api/admin/laptops/${laptopId}`)

  return response.data
}

export async function createAdminLaptop(payload) {
  const response = await request('/api/admin/laptops', {
    method: 'POST',
    body: JSON.stringify(payload),
  })

  return response.data
}

export async function updateAdminLaptop(laptopId, payload) {
  const response = await request(`/api/admin/laptops/${laptopId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })

  return response.data
}

export async function deleteAdminLaptop(laptopId) {
  const response = await request(`/api/admin/laptops/${laptopId}`, {
    method: 'DELETE',
  })

  return response.data
}

