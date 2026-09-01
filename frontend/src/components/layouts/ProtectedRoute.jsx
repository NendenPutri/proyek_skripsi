import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { LoadingState } from '../elements'
import { useAuth } from '../../hooks/useAuth'

function ProtectedRoute() {
  const location = useLocation()
  const { isAuthenticated, isCheckingSession } = useAuth()

  if (isCheckingSession) {
    return (
      <div className="admin-auth-check">
        <LoadingState message="Memvalidasi sesi admin..." />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate replace state={{ from: location }} to="/admin/login" />
  }

  return <Outlet />
}

export default ProtectedRoute

