import { Badge, EmptyState, ErrorState, LoadingState } from '../elements'
import LaptopCard from './LaptopCard'

function resolveResultPayload(result) {
  return result?.data ?? result ?? {}
}

function resolveRecommendations(payload) {
  if (Array.isArray(payload)) {
    return payload
  }

  return payload.recommendations || payload.results || payload.laptops || []
}

function RecommendationResult({ result, loading, error, onRetry }) {
  if (loading) {
    return <LoadingState message="Memuat rekomendasi..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={onRetry} />
  }

  if (!result) {
    return null
  }

  const payload = resolveResultPayload(result)
  const recommendations = resolveRecommendations(payload)
  const message = result?.message || payload.message || 'Hasil rekomendasi laptop.'
  const isAlternative = Boolean(payload.is_alternative || result?.is_alternative)
  const total = payload.total || payload.total_results || recommendations.length

  if (!recommendations.length) {
    return (
      <EmptyState
        title="Belum ada rekomendasi"
        description={message || 'Isi form rekomendasi untuk melihat hasil.'}
      />
    )
  }

  return (
    <section className="recommendation-results">
      {isAlternative ? (
        <div className="recommendation-alternative-alert">
          Tidak ditemukan laptop yang memenuhi semua kriteria. Berikut alternatif terbaik.
        </div>
      ) : null}

      <div className="recommendation-result-summary">
        <div>
          <h2 className="recommendation-result-message">{message}</h2>
          <p className="recommendation-result-total">Total hasil: {total}</p>
        </div>
        {isAlternative ? (
          <Badge className="recommendation-alternative-badge" variant="warning">
            Alternatif
          </Badge>
        ) : null}
      </div>

      <div className="recommendation-result-grid">
        {recommendations.map((laptop, index) => (
          <LaptopCard
            isBest={index === 0}
            key={laptop.id || laptop.model || index}
            laptop={laptop}
            variant="recommendation"
          />
        ))}
      </div>
    </section>
  )
}

export default RecommendationResult
