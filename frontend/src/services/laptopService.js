import { request } from './apiClient'

const laptopQueryKeys = ['limit', 'brand', 'kebutuhan', 'search']

function buildLaptopQuery(params = {}) {
  const searchParams = new URLSearchParams()

  laptopQueryKeys.forEach((key) => {
    const value = params[key]

    if (value !== undefined && value !== null && value !== '') {
      searchParams.set(key, value)
    }
  })

  const queryString = searchParams.toString()

  return queryString ? `?${queryString}` : ''
}

export function getLaptops(params = {}) {
  return request(`/api/laptops${buildLaptopQuery(params)}`)
}
