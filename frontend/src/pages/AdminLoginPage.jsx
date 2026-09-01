import { Eye, EyeOff, Laptop } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { Button, Card, ErrorState, Input, LoadingState } from '../components/elements'
import { useAuth } from '../hooks/useAuth'

const initialForm = {
  email: '',
  password: '',
}

function AdminLoginPage() {
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isPasswordVisible, setIsPasswordVisible] = useState(false)
  const { isAuthenticated, isCheckingSession, login } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const redirectTo = location.state?.from?.pathname || '/admin'

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/admin', { replace: true })
    }
  }, [isAuthenticated, navigate])

  function handleChange(event) {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      await login(form)
      navigate(redirectTo, { replace: true })
    } catch (loginError) {
      setError(loginError?.message || 'Login admin gagal. Periksa email dan password.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isCheckingSession) {
    return (
      <section className="admin-login-page">
        <LoadingState message="Memeriksa sesi admin..." />
      </section>
    )
  }

  if (isAuthenticated) {
    return <Navigate replace to="/admin" />
  }

  return (
    <section className="admin-login-page">
      <Card className="admin-login-card flex flex-col">
        <div className="admin-login-brand">
          <span className="admin-login-icon">
            <Laptop aria-hidden="true" size={24} />
          </span>
          <div>
            <p className="admin-login-eyebrow">Admin Area</p>
            <h1 className="admin-login-title">Masuk ke LaptopWise</h1>
          </div>
        </div>

        {error ? <ErrorState message={error} /> : null}

        <form className="admin-login-form" onSubmit={handleSubmit}>
          <Input
            autoComplete="email"
            label="Email Admin"
            name="email"
            onChange={handleChange}
            placeholder="admin@example.com"
            required
            type="email"
            value={form.email}
          />
          <div className="admin-password-control">
            <Input
              autoComplete="current-password"
              className="admin-password-field"
              label="Password"
              name="password"
              onChange={handleChange}
              placeholder="Masukkan password"
              required
              type={isPasswordVisible ? 'text' : 'password'}
              value={form.password}
            />
            <button
              aria-label={isPasswordVisible ? 'Sembunyikan password' : 'Tampilkan password'}
              className="admin-password-toggle"
              onClick={() => setIsPasswordVisible((currentValue) => !currentValue)}
              type="button"
            >
              {isPasswordVisible ? (
                <EyeOff aria-hidden="true" size={18} />
              ) : (
                <Eye aria-hidden="true" size={18} />
              )}
            </button>
          </div>
          <Button className="admin-login-submit" disabled={isSubmitting} type="submit">
            {isSubmitting ? 'Memproses...' : 'Login Admin'}
          </Button>
        </form>

        <Link className="admin-login-public-link" to="/">
          Kembali ke halaman publik
        </Link>
      </Card>
    </section>
  )
}

export default AdminLoginPage
