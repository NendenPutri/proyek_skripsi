import { ArrowDownUp, Eye, Pencil, Power } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Badge, Button } from '../elements'
import { formatConfidence, formatPrice, formatRating, normalizeOption } from '../../utils/formatters'

const tableColumns = [
  { label: 'Model', value: 'model' },
  { label: 'Brand', value: 'brand_name' },
  { label: 'Harga', value: 'price' },
  { label: 'Rating', value: 'rating' },
  { label: 'Kategori', value: 'predicted_category' },
  { label: 'Status', value: 'is_active' },
  { label: 'Sumber', value: 'source' },
  { label: 'Dibuat', value: 'created_at' },
]

function formatDate(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

function AdminLaptopTable({ items, onDeactivate, onSort, sortBy, sortOrder }) {
  return (
    <div className="admin-table-wrap">
      <table className="admin-table">
        <thead>
          <tr>
            {tableColumns.map((column) => (
              <th key={column.value}>
                <button
                  className="admin-sort-button"
                  onClick={() => onSort(column.value)}
                  type="button"
                >
                  {column.label}
                  <ArrowDownUp
                    aria-hidden="true"
                    className={sortBy === column.value ? 'admin-sort-active' : ''}
                    size={14}
                  />
                  {sortBy === column.value ? (
                    <span className="sr-only">Urutan {sortOrder}</span>
                  ) : null}
                </button>
              </th>
            ))}
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          {items.map((laptop) => (
            <tr key={laptop.id}>
              <td data-label="Model">
                <div className="admin-table-model">{normalizeOption(laptop.model)}</div>
                <div className="admin-table-muted">
                  {normalizeOption(laptop.processor_series)} / {normalizeOption(laptop.ram_num)} GB
                </div>
              </td>
              <td data-label="Brand">{normalizeOption(laptop.brand_name)}</td>
              <td data-label="Harga">{formatPrice(laptop)}</td>
              <td data-label="Rating">{formatRating(laptop.rating)}</td>
              <td data-label="Kategori">
                <div className="admin-table-badges">
                  <Badge>{normalizeOption(laptop.predicted_category)}</Badge>
                  {laptop.prediction_confidence !== null &&
                  laptop.prediction_confidence !== undefined ? (
                    <Badge variant="success">{formatConfidence(laptop.prediction_confidence)}</Badge>
                  ) : null}
                </div>
              </td>
              <td data-label="Status">
                <Badge variant={laptop.is_active ? 'success' : 'warning'}>
                  {laptop.is_active ? 'Aktif' : 'Nonaktif'}
                </Badge>
              </td>
              <td data-label="Sumber">{normalizeOption(laptop.source)}</td>
              <td data-label="Dibuat">{formatDate(laptop.created_at)}</td>
              <td data-label="Aksi">
                <div className="admin-table-actions">
                  <Link className="admin-action-link" to={`/admin/laptops/${laptop.id}`}>
                    <Eye aria-hidden="true" size={15} />
                    Detail
                  </Link>
                  <Link className="admin-action-link" to={`/admin/laptops/${laptop.id}/edit`}>
                    <Pencil aria-hidden="true" size={15} />
                    Edit
                  </Link>
                  <Button
                    disabled={!laptop.is_active}
                    onClick={() => onDeactivate(laptop)}
                    variant="ghost"
                  >
                    <Power aria-hidden="true" size={15} />
                    Nonaktifkan
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default AdminLaptopTable
