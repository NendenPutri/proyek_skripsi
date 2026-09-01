import { ArrowLeft, Pencil } from 'lucide-react'
import { useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { Badge, Card, ErrorState, LoadingState, Notification } from '../components/elements'
import useAdminLaptopDetail from '../hooks/useAdminLaptopDetail'
import {
  formatConfidence,
  formatOriginalPrice,
  formatPrice,
  formatRating,
  normalizeOption,
} from '../utils/formatters'

const detailFields = [
  ['Brand', 'brand_name'],
  ['Model', 'model'],
  ['Harga', 'price_idr', 'price'],
  ['Harga Original', 'price_original'],
  ['Rating', 'rating'],
  ['Processor', 'processor'],
  ['Processor Brand', 'processor_brand'],
  ['Processor Series', 'processor_series'],
  ['Processor Level', 'processor_level'],
  ['RAM', 'ram_num'],
  ['RAM Class', 'ram_class'],
  ['Memory Size', 'memory_size'],
  ['Memory Type', 'memory_type'],
  ['Storage Class', 'storage_class'],
  ['GPU Brand', 'gpu_brand'],
  ['GPU Type', 'gpu_type'],
  ['GPU Level', 'gpu_level'],
  ['OS', 'os'],
  ['OS Family', 'os_family'],
  ['Display Size', 'display_size'],
  ['Display Class', 'display_class'],
  ['Resolution', 'resolution_class'],
  ['Touch Screen', 'touchscreen_label'],
  ['Warranty Class', 'warranty_class'],
  ['Price Class', 'price_class'],
  ['Sumber Data', 'source'],
]

function getDetailValue(laptop, field, type) {
  if (type === 'price') {
    return formatPrice(laptop)
  }

  if (field === 'price_original') {
    return formatOriginalPrice(laptop.price_original, laptop.price_currency)
  }

  if (field === 'rating') {
    return formatRating(laptop.rating)
  }

  if (field === 'ram_num') {
    return laptop.ram_num ? `${laptop.ram_num} GB` : '-'
  }

  if (field === 'memory_size') {
    return laptop.memory_size ? `${laptop.memory_size} ${normalizeOption(laptop.memory_type)}` : '-'
  }

  return normalizeOption(laptop[field])
}

function AdminLaptopDetailPage() {
  const { id } = useParams()
  const location = useLocation()
  const [notification, setNotification] = useState(location.state?.notification || '')
  const { error, laptop, loading, refetch } = useAdminLaptopDetail(id)

  if (loading) {
    return <LoadingState message="Memuat detail laptop admin..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={refetch} />
  }

  return (
    <div className="admin-page-stack">
      <Notification
        message={notification}
        onClose={() => setNotification('')}
        type="success"
      />
      <div className="admin-detail-actions">
        <Link className="admin-action-link" to="/admin/laptops">
          <ArrowLeft aria-hidden="true" size={16} />
          Kembali
        </Link>
        <Link className="btn btn-primary" to={`/admin/laptops/${id}/edit`}>
          <Pencil aria-hidden="true" size={16} />
          Edit Laptop
        </Link>
      </div>

      <Card className="admin-detail-card">
        <div>
          <p className="admin-section-eyebrow">Detail Laptop</p>
          <h2 className="admin-page-title">{normalizeOption(laptop.model)}</h2>
          <p className="admin-page-description">{normalizeOption(laptop.brand_name)}</p>
        </div>
        <div className="admin-detail-badges">
          <Badge variant={laptop.is_active ? 'success' : 'warning'}>
            {laptop.is_active ? 'Aktif' : 'Nonaktif'}
          </Badge>
          <Badge>{normalizeOption(laptop.predicted_category)}</Badge>
          {laptop.prediction_confidence !== null && laptop.prediction_confidence !== undefined ? (
            <Badge variant="success">{formatConfidence(laptop.prediction_confidence)}</Badge>
          ) : null}
        </div>
      </Card>

      <Card>
        <div className="admin-detail-grid">
          {detailFields.map(([label, field, type]) => (
            <div className="admin-detail-item" key={`${label}-${field}`}>
              <span>{label}</span>
              <strong>{getDetailValue(laptop, field, type)}</strong>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}

export default AdminLaptopDetailPage
