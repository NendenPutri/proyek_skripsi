import { ShieldCheck } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { Badge, Button, Card, StatCard } from '../components/elements'
import { CategoryDistributionChart } from '../components/fragments'
import { useAuth } from '../hooks/useAuth'
import { getAdminDashboardStats } from '../services/adminDashboardService'

async function loadDashboardSummary() {
  const statsData = await getAdminDashboardStats()
  const categoryDistribution = statsData?.category_distribution || []

  return {
    categoryDistribution,
    totalActiveLaptops: categoryDistribution.reduce(
      (total, item) => total + (Number(item?.count) || 0),
      0,
    ),
  }
}

const emptySummary = {
  categoryDistribution: [],
  totalActiveLaptops: 0,
}

function AdminDashboardPage() {
  const { admin } = useAuth()
  const [summary, setSummary] = useState(emptySummary)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchDashboardSummary = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      setSummary(await loadDashboardSummary())
    } catch (requestError) {
      setSummary(emptySummary)
      setError(requestError?.message || 'Gagal memuat ringkasan dashboard admin.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let isMounted = true

    async function fetchInitialSummary() {
      try {
        const dashboardSummary = await loadDashboardSummary()

        if (isMounted) {
          setSummary(dashboardSummary)
        }
      } catch (requestError) {
        if (isMounted) {
          setSummary(emptySummary)
          setError(requestError?.message || 'Gagal memuat ringkasan dashboard admin.')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchInitialSummary()

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <div className="admin-dashboard">
      <section className="admin-welcome-card">
        <div className="admin-welcome-copy">
          <p className="admin-section-eyebrow">Sesi tervalidasi</p>
          <h2 className="admin-page-title">Selamat datang, {admin?.name || 'Admin'}</h2>
          <p className="admin-page-description">
            Pantau ringkasan data laptop yang sedang aktif dan lihat sebaran kategori
            kebutuhan untuk membantu pengelolaan katalog.
          </p>
        </div>
        <div className="admin-welcome-actions">
          <Badge variant={admin?.is_active ? 'success' : 'warning'}>
            {admin?.is_active ? 'Admin Aktif' : 'Status tidak aktif'}
          </Badge>
          <Button onClick={fetchDashboardSummary} variant="ghost">
            Refresh Statistik
          </Button>
        </div>
      </section>

      <div className="admin-stat-grid">
        <StatCard
          description="Jumlah laptop aktif yang tersedia untuk ditampilkan kepada pengguna."
          label="Laptop Aktif Terhitung"
          value={loading ? '...' : summary.totalActiveLaptops}
        />
        <StatCard
          description="Akun yang sedang digunakan untuk mengelola data laptop."
          label="Admin Login"
          value={admin?.name || '-'}
        />
      </div>

      <CategoryDistributionChart
        data={summary.categoryDistribution}
        error={error}
        loading={loading}
        onRetry={fetchDashboardSummary}
      />

      <Card className="admin-info-card">
        <div className="admin-info-icon">
          <ShieldCheck aria-hidden="true" size={22} />
        </div>
        <div>
          <h3>Autentikasi aktif</h3>
          <p>
            Sesi admin sedang aktif. Jika sesi berakhir, Anda akan diarahkan kembali ke
            halaman login untuk menjaga keamanan area pengelolaan.
          </p>
        </div>
      </Card>
    </div>
  )
}

export default AdminDashboardPage
