import { clearAdminAccessToken, getAdminAccessToken } from '../utils/authStorage'
import { API_BASE_URL, buildApiUrl } from '../config/api'

export class ApiError extends Error {
  constructor(message, { status, body, isUnauthorized = false, cause } = {}) {
    super(message, { cause })
    this.name = 'ApiError'
    this.status = status
    this.body = body
    this.isUnauthorized = isUnauthorized
  }
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || ''

  if (!contentType.includes('application/json')) {
    return null
  }

  return response.json()
}

export async function request(endpoint, options = {}) {
  const { headers, skipAuth = false, ...requestOptions } = options
  const token = skipAuth ? null : getAdminAccessToken()

  let response

  try {
    response = await fetch(buildApiUrl(endpoint), {
      ...requestOptions,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...headers,
      },
    })
  } catch (error) {
    throw new ApiError(
      error?.message
        ? `Tidak dapat terhubung ke layanan aplikasi: ${error.message}`
        : 'Tidak dapat terhubung ke layanan aplikasi. Pastikan server sedang aktif.',
      { cause: error },
    )
  }

  const body = await parseResponse(response)
  const backendMessage = body?.message
  const errorDetail = typeof body?.detail === 'string' ? body.detail : null

  if (!response.ok) {
    if (response.status === 401) {
      clearAdminAccessToken()
      window.dispatchEvent(new Event('admin-session-expired'))
    }

    throw new ApiError(
      backendMessage ||
        errorDetail ||
        `Request gagal dengan status ${response.status} ${response.statusText}`.trim(),
      {
        status: response.status,
        body,
        isUnauthorized: response.status === 401,
      },
    )
  }

  if (body && body.success === false) {
    throw new ApiError(backendMessage || 'Layanan aplikasi belum berhasil memproses permintaan.', {
      status: response.status,
      body,
    })
  }

  return body
}

export { API_BASE_URL }
