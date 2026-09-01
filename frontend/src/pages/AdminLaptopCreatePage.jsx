import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ErrorState, Notification } from '../components/elements'
import { AdminLaptopForm } from '../components/fragments'
import useOptions from '../hooks/useOptions'
import { createAdminLaptop } from '../services/adminLaptopService'
import {
  ADMIN_LAPTOP_DEFAULT_FORM,
  serializeAdminLaptopForm,
  validateAdminLaptopForm,
} from '../utils/adminLaptopForm'
import { formatConfidence, normalizeOption } from '../utils/formatters'

function AdminLaptopCreatePage() {
  const [form, setForm] = useState(ADMIN_LAPTOP_DEFAULT_FORM)
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [notification, setNotification] = useState(null)
  const navigate = useNavigate()
  const { error: optionsError, loading: optionsLoading, options } = useOptions()

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
      const createdLaptop = await createAdminLaptop(serializeAdminLaptopForm(form))
      const confidenceText =
        createdLaptop.prediction_confidence !== null &&
        createdLaptop.prediction_confidence !== undefined
          ? ` (${formatConfidence(createdLaptop.prediction_confidence)})`
          : ''

      const successMessage = `Laptop berhasil ditambahkan. Prediksi: ${normalizeOption(
        createdLaptop.predicted_category,
      )}${confidenceText}.`

      setNotification({
        message: successMessage,
        type: 'success',
      })
      navigate(`/admin/laptops/${createdLaptop.id}`, {
        replace: true,
        state: { notification: successMessage },
      })
    } catch (requestError) {
      setNotification({
        message: requestError?.message || 'Laptop gagal ditambahkan.',
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
          <p className="admin-section-eyebrow">Tambah Laptop</p>
          <h2 className="admin-page-title">Input Manual Laptop</h2>
          <p className="admin-page-description">
            Isi data laptop dengan lengkap. Kategori akan ditentukan otomatis setelah
            data berhasil disimpan.
          </p>
        </div>
        <Link className="btn btn-secondary" to="/admin/laptops">
          Kembali ke daftar
        </Link>
      </section>

      {optionsError ? <ErrorState message={optionsError} /> : null}

      <AdminLaptopForm
        backendOptions={options || {}}
        errors={errors}
        form={form}
        onChange={handleChange}
        onSubmit={handleSubmit}
        submitLabel={optionsLoading ? 'Memuat pilihan...' : 'Tambah Laptop'}
        submitting={submitting || optionsLoading}
      />
    </div>
  )
}

export default AdminLaptopCreatePage
