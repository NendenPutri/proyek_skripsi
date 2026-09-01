import { ErrorState } from '../components/elements'
import { RecommendationForm, RecommendationResult } from '../components/fragments'
import useOptions from '../hooks/useOptions'
import useRecommendations from '../hooks/useRecommendations'

function RecommendationPage() {
  const {
    options,
    loading: optionsLoading,
    error: optionsError,
    refetch,
  } = useOptions()
  const {
    result,
    loading: recommendationLoading,
    error: recommendationError,
    lastPayload,
    submitRecommendation,
    resetResult,
  } = useRecommendations()

  return (
    <section className="recommendation-page">
      <div className="container-app">
        <header className="recommendation-header">
          <p className="recommendation-eyebrow">Rekomendasi</p>
          <h1 className="recommendation-title">Cari Rekomendasi <span class="hero-highlight">Laptop</span></h1>
          <p className="recommendation-description">
            Isi kebutuhan penggunaan, budget, dan spesifikasi utama. Sistem akan
            menampilkan rekomendasi laptop berdasarkan data dan model Naive Bayes.
          </p>
        </header>

        {optionsError ? (
          <div className="recommendation-alert">
            <ErrorState message={optionsError} onRetry={refetch} />
          </div>
        ) : null}

        <RecommendationForm
          loading={optionsLoading || recommendationLoading}
          onReset={resetResult}
          onSubmit={submitRecommendation}
          options={options}
        />

        <RecommendationResult
          error={recommendationError}
          loading={recommendationLoading}
          onRetry={lastPayload ? () => submitRecommendation(lastPayload) : undefined}
          result={result}
        />
      </div>
    </section>
  )
}

export default RecommendationPage
