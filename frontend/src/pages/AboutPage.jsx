import { useEffect, useMemo, useState } from 'react'
import {
  Badge,
  Card,
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatCard,
} from '../components/elements'
import { getModelInfo } from '../services/modelInfoService'
import { NEED_LABELS } from '../utils/constants'
import { formatScore, normalizeOption } from '../utils/formatters'

const technologies = [
  'ReactJS',
  'FastAPI',
  'Naive Bayes',
  'Dataset hasil preprocessing',
]

function resolveModelInfo(response) {
  return response?.data ?? response ?? null
}

function resolveMetrics(modelInfo) {
  const metrics = modelInfo?.metrics || modelInfo?.model_metrics || modelInfo?.evaluation || {}

  return Object.entries(metrics)
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .slice(0, 4)
}

function formatMetricValue(value) {
  return typeof value === 'number' ? formatScore(value) : normalizeOption(value)
}

function AboutPage() {
  const [modelInfo, setModelInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [refreshKey, setRefreshKey] = useState(0)
  const metrics = useMemo(() => resolveMetrics(modelInfo), [modelInfo])

  useEffect(() => {
    let isMounted = true

    async function fetchModelInfo() {
      try {
        const response = await getModelInfo()

        if (isMounted) {
          setModelInfo(resolveModelInfo(response))
          setError('')
        }
      } catch (requestError) {
        if (isMounted) {
          setModelInfo(null)
          setError(
            requestError?.message
              ? `Gagal memuat info model: ${requestError.message}`
              : 'Gagal memuat info model. Pastikan layanan aplikasi sedang aktif.',
          )
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchModelInfo()

    return () => {
      isMounted = false
    }
  }, [refreshKey])

  function handleRetry() {
    setLoading(true)
    setRefreshKey((currentKey) => currentKey + 1)
  }

  return (
    <section className="section">
      <div className="container-app">
        <PageHeader
          description="Sistem ini membantu pengguna memilih laptop berdasarkan kebutuhan dengan data dan proses rekomendasi yang terpusat."
          eyebrow="Tentang Sistem"
          title="Sistem Rekomendasi Laptop"
        />

        <div className="stack-panel">
          <Card>
            <h2 className="section-heading">Ringkasan</h2>
            <p className="section-description">
              Sistem menggunakan data laptop hasil preprocessing dan model Naive
              Bayes untuk membantu mencocokkan laptop dengan kebutuhan pengguna.
              Aplikasi menampilkan form, data laptop, status layanan, dan hasil
              rekomendasi tanpa membaca dataset atau model secara langsung.
            </p>
          </Card>

          <Card>
            <h2 className="section-heading">Teknologi</h2>
            <div className="info-list">
              {technologies.map((technology) => (
                <div className="info-item" key={technology}>
                  <Badge variant="muted">{technology}</Badge>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <h2 className="section-heading">Label Kebutuhan</h2>
            <div className="label-stack">
              {NEED_LABELS.map((label) => (
                <Badge key={label} variant="success">
                  {label}
                </Badge>
              ))}
            </div>
            <p className="field-helper">
              Harga laptop ditampilkan dalam Rupiah berdasarkan hasil konversi
              pada tahap preprocessing dataset. Harga asli dataset tetap disimpan
              sebagai informasi tambahan jika tersedia.
            </p>
          </Card>

          {loading ? <LoadingState message="Memuat informasi model..." /> : null}
          {!loading && error ? <ErrorState message={error} onRetry={handleRetry} /> : null}
          {!loading && !error && !modelInfo ? (
            <EmptyState
              description="Informasi model belum tersedia dari layanan aplikasi."
              title="Info model belum tersedia"
            />
          ) : null}
          {!loading && !error && modelInfo ? (
            <Card>
              <h2 className="section-heading">Informasi Model</h2>
              <div className="info-list">
                <div className="info-item">
                  <p className="spec-label">Nama Model</p>
                  <p className="info-value">
                    {normalizeOption(modelInfo.model_name || modelInfo.name || 'Naive Bayes')}
                  </p>
                </div>
                <div className="info-item">
                  <p className="spec-label">Status</p>
                  <p className="info-value">
                    {normalizeOption(modelInfo.status || modelInfo.message || 'Tersedia')}
                  </p>
                </div>
              </div>

              {metrics.length ? (
                <div className="metric-grid mt-6">
                  {metrics.map(([label, value]) => (
                    <StatCard
                      description="Metrik evaluasi model"
                      key={label}
                      label={label}
                      value={formatMetricValue(value)}
                    />
                  ))}
                </div>
              ) : (
                <EmptyState
                  description="Endpoint model-info belum menyertakan metrik evaluasi."
                  title="Metrik model belum tersedia"
                />
              )}
            </Card>
          ) : null}
        </div>
      </div>
    </section>
  )
}

export default AboutPage
