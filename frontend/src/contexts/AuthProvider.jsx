import { useCallback, useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCurrentAdmin, loginAdmin } from '../services/adminAuthService'
import {
  clearAdminAccessToken,
  hasAdminAccessToken,
  setAdminAccessToken,
} from '../utils/authStorage'
import { AuthContext } from './AuthContext'

const initialStatus = hasAdminAccessToken() ? 'checking' : 'guest'

function AuthProvider({ children }) {
  const [admin, setAdmin] = useState(null)
  const [status, setStatus] = useState(initialStatus)
  const navigate = useNavigate()

  const clearSession = useCallback(() => {
    clearAdminAccessToken()
    setAdmin(null)
    setStatus('guest')
  }, [])

  const validateSession = useCallback(async ({ markChecking = true } = {}) => {
    if (!hasAdminAccessToken()) {
      clearSession()
      return null
    }

    if (markChecking) {
      setStatus('checking')
    }

    try {
      const currentAdmin = await getCurrentAdmin()
      setAdmin(currentAdmin)
      setStatus('authenticated')
      return currentAdmin
    } catch {
      clearSession()
      return null
    }
  }, [clearSession])

  const login = useCallback(async ({ email, password }) => {
    const loginResult = await loginAdmin({ email, password })
    setAdminAccessToken(loginResult.access_token)
    setAdmin(loginResult.admin)
    setStatus('authenticated')
    return loginResult.admin
  }, [])

  const logout = useCallback(() => {
    clearSession()
    navigate('/admin/login', { replace: true })
  }, [clearSession, navigate])

  useEffect(() => {
    let isMounted = true

    async function validateInitialSession() {
      if (!hasAdminAccessToken()) {
        return
      }

      try {
        const currentAdmin = await getCurrentAdmin()

        if (!isMounted) {
          return
        }

        setAdmin(currentAdmin)
        setStatus('authenticated')
      } catch {
        if (isMounted) {
          clearSession()
        }
      }
    }

    validateInitialSession()

    return () => {
      isMounted = false
    }
  }, [clearSession])

  useEffect(() => {
    function handleSessionExpired() {
      clearSession()
      navigate('/admin/login', { replace: true })
    }

    window.addEventListener('admin-session-expired', handleSessionExpired)

    return () => {
      window.removeEventListener('admin-session-expired', handleSessionExpired)
    }
  }, [clearSession, navigate])

  const value = useMemo(
    () => ({
      admin,
      isAuthenticated: status === 'authenticated',
      isCheckingSession: status === 'checking',
      login,
      logout,
      status,
      validateSession,
    }),
    [admin, login, logout, status, validateSession],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthProvider

