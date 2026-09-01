import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ErrorState, LoadingState, Notification } from '../components/elements'
import { AdminLaptopForm } from '../components/fragments'
import useAdminLaptopDetail from '../hooks/useAdminLaptopDetail'
import useOptions from '../hooks/useOptions'
import { updateAdminLaptop } from '../services/adminLaptopService'
import {
  mapLaptopToAdminForm,
  serializeAdminLaptopForm,
  validateAdminLaptopForm,
} from '../utils/adminLaptopForm'
import { formatConfidence, normalizeOption } from '../utils/formatters'

function AdminLaptopEditFormContent({ id, laptop, options, optionsError, optionsLoading }) {
  const [form, setForm] = useState(() => mapLaptopToAdminForm(laptop))
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [notification, setNotification] = useState(null)
  const navigate = useNavigate()

  function handleChange(event) {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
    setErrors((currentErrors) => ({ ...currentErrors, [name]: '' }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const validationErrors = validateAdminLaptopForm(form)

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      return
    }

    setSubmitting(true)
    setErrors({})

    try {
      const updatedLaptop = await updateAdminLaptop(id, serializeAdminLaptopForm(form))
      const confidenceText =
        updatedLaptop.prediction_confidence !== null &&
        updatedLaptop.prediction_confidence !== undefined
          ? ` (${formatConfidence(updatedLaptop.prediction_confidence)})`
          : ''

      const successMessage = `Laptop berhasil diperbarui. Prediksi: ${normalizeOption(
        updatedLaptop.predicted_category,
      )}${confidenceText}.`

      setNotification({
        message: successMessage,
        type: 'success',
      })
      navigate(`/admin/laptops/${updatedLaptop.id}`, {
        replace: true,
        state: { notification: successMessage },
      })
    } catch (requestError) {
      setNotification({
        message: requestError?.message || 'Laptop gagal diperbarui.',
        type: 'error',
      })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="admin-page-stack">
      <Notification
        message={notification?.message}
        onClose={() => setNotification(null)}
        type={notification?.type}
      />
      <section className="admin-page-heading-row">
        <div>
          <p className="admin-section-eyebrow">Edit Laptop</p>
          <h2 className="admin-page-title">{normalizeOption(laptop.model)}</h2>
          <p className="admin-page-description">
            Perbarui data laptop dengan teliti. Jika spesifikasi utama berubah,
            kategori akan diperbarui otomatis.
          </p>
        </div>
        <Link className="btn btn-secondary" to={`/admin/laptops/${id}`}>
          Kembali ke detail
        </Link>
      </section>

      {optionsError ? <ErrorState message={optionsError} /> : null}

      <AdminLaptopForm
        backendOptions={options || {}}
        errors={errors}
        form={form}
        onChange={handleChange}
        onSubmit={handleSubmit}
        submitLabel={optionsLoading ? 'Memuat pilihan...' : 'Simpan Perubahan'}
        submitting={submitting || optionsLoading}
      />
    </div>
  )
}

function AdminLaptopEditPage() {
  const { id } = useParams()
  const { error, laptop, loading, refetch } = useAdminLaptopDetail(id)
  const { error: optionsError, loading: optionsLoading, options } = useOptions()

  if (loading || !laptop) {
    return <LoadingState message="Memuat form edit laptop..." />
  }

  if (error) {
    return <ErrorState message={error} onRetry={refetch} />
  }

  return (
    <AdminLaptopEditFormContent
      id={id}
      laptop={laptop}
      options={options}
      optionsError={optionsError}
      optionsLoading={optionsLoading}
    />
  )
}

export default AdminLaptopEditPage
