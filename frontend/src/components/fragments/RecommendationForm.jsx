import { Search } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Button, Card, ConfirmDialog, Select } from '../elements'
import {
  DEFAULT_ALL_OPTION,
  DEFAULT_RECOMMENDATION_PAYLOAD,
  FALLBACK_RECOMMENDATION_OPTIONS,
} from '../../utils/constants'
import { formatRupiah } from '../../utils/formatters'

const numericFields = ['budget_maksimal', 'ram_min', 'storage_min', 'jumlah_hasil']

function isOptionsAvailable(options) {
  return Boolean(options && typeof options === 'object' && Object.keys(options).length)
}

function getOptionList(options, key) {
  const optionValue = options?.[key]

  if (Array.isArray(optionValue) && optionValue.length) {
    return optionValue
  }

  return FALLBACK_RECOMMENDATION_OPTIONS[key] || []
}

function getOptionValue(option) {
  if (typeof option === 'object' && option !== null) {
    return option.value ?? option.label
  }

  return option
}

function withDefaultOption(optionList, defaultOption) {
  const hasDefaultOption = optionList.some((option) => getOptionValue(option) === defaultOption)

  return hasDefaultOption ? optionList : [defaultOption, ...optionList]
}

function normalizeBudgetOptions(optionList) {
  return optionList.map((option) => {
    const value = getOptionValue(option)

    if (typeof option === 'object' && option !== null && option.label) {
      return option
    }

    return {
      label: value === '' || value === null ? 'Semua budget' : `Maksimal ${formatRupiah(value)}`,
      value: value ?? '',
    }
  })
}

function normalizeNumericValue(value) {
  if (value === '' || value === DEFAULT_ALL_OPTION || value === null || value === undefined) {
    return null
  }

  return Number(value)
}

function validateForm(form) {
  const errors = {}

  if (!form.kebutuhan) {
    errors.kebutuhan = 'Kebutuhan wajib dipilih.'
  }

  if (form.budget_maksimal !== '') {
    const budget = Number(form.budget_maksimal)

    if (!Number.isFinite(budget) || budget <= 0) {
      errors.budget_maksimal = 'Budget harus berupa angka lebih dari 0.'
    }
  }

  numericFields.forEach((field) => {
    const value = normalizeNumericValue(form[field])

    if (value !== null && value < 0) {
      errors[field] = 'Angka tidak boleh negatif.'
    }
  })

  const jumlahHasil = Number(form.jumlah_hasil)

  if (!Number.isFinite(jumlahHasil) || jumlahHasil < 1 || jumlahHasil > 50) {
    errors.jumlah_hasil = 'Jumlah hasil harus antara 1 sampai 50.'
  }

  return errors
}

function buildRecommendationPayload(form) {
  return {
    kebutuhan: form.kebutuhan,
    budget_maksimal: normalizeNumericValue(form.budget_maksimal),
    ram_min: normalizeNumericValue(form.ram_min),
    storage_min: normalizeNumericValue(form.storage_min),
    brand: form.brand || DEFAULT_ALL_OPTION,
    os_family: form.os_family || DEFAULT_ALL_OPTION,
    processor_min_level: form.processor_min_level || DEFAULT_ALL_OPTION,
    gpu_type: form.gpu_type || 'Tidak wajib',
    touch_screen: form.touch_screen || DEFAULT_ALL_OPTION,
    jumlah_hasil: Number(form.jumlah_hasil),
  }
}

function RecommendationForm({ options, loading = false, onSubmit, onReset }) {
  const [form, setForm] = useState(DEFAULT_RECOMMENDATION_PAYLOAD)
  const [errors, setErrors] = useState({})
  const [isResetDialogOpen, setIsResetDialogOpen] = useState(false)
  const hasBackendOptions = isOptionsAvailable(options)
  const formOptions = useMemo(
    () => ({
      kebutuhan: getOptionList(options, 'kebutuhan'),
      budget_options: normalizeBudgetOptions(getOptionList(options, 'budget_options')),
      brand: withDefaultOption(getOptionList(options, 'brand'), DEFAULT_ALL_OPTION),
      processor_level: withDefaultOption(getOptionList(options, 'processor_level'), DEFAULT_ALL_OPTION),
      ram_min: withDefaultOption(getOptionList(options, 'ram_min'), DEFAULT_ALL_OPTION),
      storage_min: withDefaultOption(getOptionList(options, 'storage_min'), DEFAULT_ALL_OPTION),
      gpu_type: withDefaultOption(getOptionList(options, 'gpu_type'), 'Tidak wajib'),
      os_family: withDefaultOption(getOptionList(options, 'os_family'), DEFAULT_ALL_OPTION),
      touch_screen: withDefaultOption(getOptionList(options, 'touch_screen'), DEFAULT_ALL_OPTION),
      jumlah_hasil: getOptionList(options, 'jumlah_hasil'),
    }),
    [options],
  )

  function handleChange(event) {
    const { name, value } = event.target

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
    setErrors((currentErrors) => ({
      ...currentErrors,
      [name]: '',
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nextErrors = validateForm(form)
    setErrors(nextErrors)

    if (Object.values(nextErrors).some(Boolean)) {
      return
    }

    await onSubmit(buildRecommendationPayload(form))
  }

  function handleReset() {
    setForm(DEFAULT_RECOMMENDATION_PAYLOAD)
    setErrors({})
    onReset?.()
  }

  function handleResetRequest() {
    setIsResetDialogOpen(true)
  }

  function handleResetConfirm() {
    setIsResetDialogOpen(false)
    handleReset()
  }

  return (
    <Card className="recommendation-form-card">
      {!hasBackendOptions ? (
        <div className="form-note">
          Pilihan form belum termuat sepenuhnya. Beberapa pilihan dasar tetap
          tersedia agar Anda bisa mulai mengisi kebutuhan laptop.
        </div>
      ) : null}

      <form onSubmit={handleSubmit}>
        <div className="recommendation-form-grid">
          <Select
            error={errors.kebutuhan}
            label="Kebutuhan"
            name="kebutuhan"
            onChange={handleChange}
            options={formOptions.kebutuhan}
            value={form.kebutuhan}
          />

          <Select
            error={errors.budget_maksimal}
            helper="Pilih batas harga maksimal dalam Rupiah."
            label="Budget Maksimal"
            name="budget_maksimal"
            onChange={handleChange}
            options={formOptions.budget_options}
            value={form.budget_maksimal}
          />

          <Select
            error={errors.ram_min}
            label="RAM Minimum"
            name="ram_min"
            onChange={handleChange}
            options={formOptions.ram_min}
            value={form.ram_min}
          />

          <Select
            error={errors.storage_min}
            label="Storage Minimum"
            name="storage_min"
            onChange={handleChange}
            options={formOptions.storage_min}
            value={form.storage_min}
          />

          <Select
            label="Brand"
            name="brand"
            onChange={handleChange}
            options={formOptions.brand}
            value={form.brand}
          />

          <Select
            label="Sistem Operasi"
            name="os_family"
            onChange={handleChange}
            options={formOptions.os_family}
            value={form.os_family}
          />

          <Select
            label="Level Processor Minimum"
            name="processor_min_level"
            onChange={handleChange}
            options={formOptions.processor_level}
            value={form.processor_min_level}
          />

          <Select
            label="Tipe GPU"
            name="gpu_type"
            onChange={handleChange}
            options={formOptions.gpu_type}
            value={form.gpu_type}
          />

          <Select
            label="Touch Screen"
            name="touch_screen"
            onChange={handleChange}
            options={formOptions.touch_screen}
            value={form.touch_screen}
          />

          <Select
            error={errors.jumlah_hasil}
            label="Jumlah Hasil"
            name="jumlah_hasil"
            onChange={handleChange}
            options={formOptions.jumlah_hasil}
            value={form.jumlah_hasil}
          />
        </div>

        <div className="recommendation-form-actions">
          <Button className="recommendation-submit" disabled={loading} type="submit">
            <Search aria-hidden="true" size={16} />
            {loading ? 'Memproses...' : 'Dapatkan Rekomendasi'}
          </Button>
          <Button
            className="recommendation-reset"
            disabled={loading}
            onClick={handleResetRequest}
            variant="ghost"
          >
            Reset Form
          </Button>
        </div>
      </form>

      {isResetDialogOpen ? (
        <ConfirmDialog
          confirmLabel="Reset Form"
          description="Semua pilihan pada form rekomendasi akan dikembalikan ke nilai awal dan hasil yang sedang tampil akan dibersihkan."
          onCancel={() => setIsResetDialogOpen(false)}
          onConfirm={handleResetConfirm}
          title="Reset form rekomendasi?"
        />
      ) : null}
    </Card>
  )
}

export default RecommendationForm
