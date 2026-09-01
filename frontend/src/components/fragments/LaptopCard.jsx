import { Star, Verified } from 'lucide-react'
import { Badge, Card } from '../elements'
import {
  formatCompactScore,
  formatConfidence,
  formatOriginalPrice,
  formatPrice,
  formatRating,
  normalizeOption,
} from '../../utils/formatters'

function getLaptopValue(laptop, keys) {
  const key = keys.find((candidate) => laptop?.[candidate] !== undefined && laptop?.[candidate] !== null)

  return key ? laptop[key] : undefined
}

function SpecRow({ label, value }) {
  return (
    <div className="spec-row">
      <span className="spec-label">{label}</span>
      <span className="spec-value">{normalizeOption(value)}</span>
    </div>
  )
}

function PriceDisplay({ laptop, className = '' }) {
  const hasIdrPrice =
    laptop?.price_idr !== undefined &&
    laptop?.price_idr !== null &&
    laptop?.price_idr !== '' &&
    Number.isFinite(Number(laptop.price_idr))
  const primaryPrice = formatPrice(laptop)
  const originalPrice = formatOriginalPrice(laptop?.price_original, laptop?.price_currency)

  return (
    <div className={className}>
      <span className="price-text">{hasIdrPrice ? `Harga ${primaryPrice}` : primaryPrice}</span>
      {originalPrice !== '-' ? (
        <span className="price-meta">{originalPrice}</span>
      ) : null}
    </div>
  )
}

function RecommendationLaptopCard({ laptop, isBest }) {
  const model = laptop?.model
  const brandName = laptop?.brand_name
  const predictedLabel = laptop?.backend_predicted_label
  const confidence = laptop?.backend_confidence
  const finalScore = laptop?.final_score
  const reason = laptop?.alasan_rekomendasi
  const isExactMatch = laptop?.is_exact_match === true
  const matchPercentage = laptop?.match_percentage
  const unmetFilters = Array.isArray(laptop?.unmet_filters) ? laptop.unmet_filters : []
  const memorySize = laptop?.memory_size
  const memoryType = laptop?.memory_type
  const memoryText = [memorySize, memoryType].map(normalizeOption).filter((value) => value !== '-').join(' ')

  return (
    <article className={`recommendation-laptop-card ${isBest && isExactMatch ? 'recommendation-laptop-best' : ''}`}>
      {!isExactMatch ? (
        <span className="recommendation-match recommendation-item-alternative">
          Alternatif
        </span>
      ) : isBest ? (
        <span className="recommendation-match recommendation-best-match">
          <Verified aria-hidden="true" size={14} />
          Best Match
        </span>
      ) : matchPercentage !== undefined && matchPercentage !== null ? (
        <span className="recommendation-match">{formatCompactScore(matchPercentage)}% Match</span>
      ) : confidence !== undefined ? (
        <span className="recommendation-match">{formatConfidence(confidence)}</span>
      ) : null}

      <div className="recommendation-card-heading">
        <p className="recommendation-brand">{normalizeOption(brandName)}</p>
        <h3 className="recommendation-model">{normalizeOption(model)}</h3>
      </div>

      <div className="recommendation-card-badges">
        <PriceDisplay className="recommendation-price" laptop={laptop} />
        <Badge className="recommendation-rating" variant="warning">
          <Star aria-hidden="true" size={12} />
          Rating {formatRating(laptop?.rating)}
        </Badge>
        {predictedLabel !== undefined ? (
          <Badge className="recommendation-label" variant="muted">
            {normalizeOption(predictedLabel)}
          </Badge>
        ) : null}
      </div>

      <div className="recommendation-spec-list">
        <SpecRow label="Processor" value={laptop?.processor_series} />
        <SpecRow label="Level Processor" value={laptop?.processor_level} />
        <SpecRow label="RAM" value={laptop?.ram_num} />
        <SpecRow label="Storage" value={memoryText} />
        <SpecRow label="GPU" value={laptop?.gpu_type} />
        <SpecRow label="Level GPU" value={laptop?.gpu_level} />
        <SpecRow label="OS" value={laptop?.os_family} />
        <SpecRow label="Confidence" value={formatConfidence(confidence)} />
        <SpecRow label="Final Score" value={formatCompactScore(finalScore)} />
        <SpecRow label="Match" value={matchPercentage !== undefined && matchPercentage !== null ? `${formatCompactScore(matchPercentage)}%` : '-'} />
      </div>

      {unmetFilters.length ? (
        <div className="unmet-filter-box">
          <p className="unmet-filter-title">Filter belum terpenuhi:</p>
          <ul className="unmet-filter-list">
            {unmetFilters.map((filter) => (
              <li key={filter}>{filter}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <p className="recommendation-reason">
        <strong>Alasan:</strong>{' '}
        {reason || 'Alasan rekomendasi tidak tersedia.'}
      </p>
    </article>
  )
}

function CatalogLaptopCard({ laptop }) {
  const model = getLaptopValue(laptop, ['model', 'laptop_model', 'name'])
  const brandName = getLaptopValue(laptop, ['brand_name', 'brand'])
  const label = getLaptopValue(laptop, [
    'label_kebutuhan',
    'predicted_label',
    'predictedLabel',
    'backend_predicted_label',
    'label',
    'kebutuhan',
  ])
  const memorySize = getLaptopValue(laptop, ['memory_size', 'storage_size'])
  const memoryType = getLaptopValue(laptop, ['memory_type', 'storage_type'])
  const memoryText = [memorySize, memoryType].map(normalizeOption).filter((value) => value !== '-').join(' ')

  return (
    <article className="catalog-laptop-card">
      <div className="catalog-card-heading">
        <span className="catalog-brand">{normalizeOption(brandName)}</span>
        {label ? <span className="catalog-label">{label}</span> : null}
      </div>

      <h3 className="catalog-model">{normalizeOption(model)}</h3>

      <div className="catalog-badges">
        <PriceDisplay className="catalog-price" laptop={laptop} />
        <Badge className="catalog-rating" variant="warning">
          <Star aria-hidden="true" size={12} />
          Rating {formatRating(laptop?.rating)}
        </Badge>
      </div>

      <div className="catalog-spec-list">
        <SpecRow label="Processor" value={laptop?.processor_series} />
        <SpecRow label="Level Processor" value={laptop?.processor_level} />
        <SpecRow label="RAM" value={laptop?.ram_num} />
        <SpecRow label="Storage" value={memoryText} />
        <SpecRow label="GPU" value={laptop?.gpu_type} />
        <SpecRow label="Level GPU" value={laptop?.gpu_level} />
        <SpecRow label="OS" value={laptop?.os_family} />
      </div>
    </article>
  )
}

function LaptopCard({ laptop, variant = 'default', isBest = false }) {
  if (variant === 'recommendation') {
    return <RecommendationLaptopCard isBest={isBest} laptop={laptop} />
  }

  if (variant === 'catalog') {
    return <CatalogLaptopCard laptop={laptop} />
  }

  const model = getLaptopValue(laptop, ['model', 'laptop_model', 'name'])
  const brandName = getLaptopValue(laptop, ['brand_name', 'brand'])
  const label = getLaptopValue(laptop, ['predicted_label', 'predictedLabel', 'label', 'kebutuhan'])
  const confidence = getLaptopValue(laptop, ['confidence', 'confidence_score', 'probability'])
  const memorySize = getLaptopValue(laptop, ['memory_size', 'storage_size'])
  const memoryType = getLaptopValue(laptop, ['memory_type', 'storage_type'])
  const memoryText = [memorySize, memoryType].map(normalizeOption).filter((value) => value !== '-').join(' ')

  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-indigo-600">{normalizeOption(brandName)}</p>
          <h3 className="mt-1 text-xl font-bold text-slate-950">{normalizeOption(model)}</h3>
        </div>
        {label ? <Badge variant="muted">{label}</Badge> : null}
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <PriceDisplay laptop={laptop} />
        <Badge variant="warning">Rating {formatRating(laptop?.rating)}</Badge>
        {confidence !== undefined ? (
          <Badge variant="muted">Confidence {formatConfidence(confidence)}</Badge>
        ) : null}
      </div>

      <div className="spec-list">
        <SpecRow label="Processor" value={laptop?.processor_series} />
        <SpecRow label="Level Processor" value={laptop?.processor_level} />
        <SpecRow label="RAM" value={laptop?.ram_num} />
        <SpecRow label="Storage" value={memoryText} />
        <SpecRow label="GPU" value={laptop?.gpu_type} />
        <SpecRow label="Level GPU" value={laptop?.gpu_level} />
        <SpecRow label="OS" value={laptop?.os_family} />
      </div>
    </Card>
  )
}

export default LaptopCard
