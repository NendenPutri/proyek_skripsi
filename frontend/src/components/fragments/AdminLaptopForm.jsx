import { Button, Card, Input, Select } from '../elements'
import { ADMIN_LAPTOP_FIELD_GROUPS } from '../../utils/adminLaptopForm'

function buildOptions(field, backendOptions = {}) {
  if (field.options) {
    return [{ label: 'Pilih opsi', value: '' }, ...field.options]
  }

  const values = backendOptions[field.optionKey] || []
  return [
    { label: 'Pilih opsi', value: '' },
    ...values
      .filter((value) => value !== 'Semua')
      .map((value) => ({
        label: String(value),
        value,
      })),
  ]
}

function AdminLaptopForm({
  backendOptions,
  errors = {},
  form,
  onChange,
  onSubmit,
  submitLabel,
  submitting = false,
}) {
  function renderField(field) {
    const commonProps = {
      error: errors[field.name],
      helper: field.required ? 'Wajib diisi agar data laptop dapat disimpan.' : undefined,
      label: field.label,
      name: field.name,
      onChange,
      value: form[field.name],
    }

    if (field.type === 'select') {
      return (
        <Select
          {...commonProps}
          options={buildOptions(field, backendOptions)}
        />
      )
    }

    return (
      <Input
        {...commonProps}
        max={field.max}
        min={field.min}
        type={field.inputType || 'text'}
      />
    )
  }

  return (
    <form className="admin-form-stack" onSubmit={onSubmit}>
      <Card className="admin-form-note-card">
        <strong>Kategori tidak dipilih manual.</strong>
        <p>
          Sistem akan menentukan kategori laptop secara otomatis setelah data disimpan.
          Nilai keyakinan prediksi akan ditampilkan jika tersedia.
        </p>
      </Card>

      {ADMIN_LAPTOP_FIELD_GROUPS.map((group) => (
        <Card className="admin-form-card" key={group.title}>
          <div className="admin-form-heading">
            <h2>{group.title}</h2>
            <p>{group.description}</p>
          </div>
          <div className="admin-form-grid">
            {group.fields.map((field) => (
              <div key={field.name}>{renderField(field)}</div>
            ))}
          </div>
        </Card>
      ))}

      <div className="admin-form-actions">
        <Button disabled={submitting} type="submit">
          {submitting ? 'Menyimpan...' : submitLabel}
        </Button>
      </div>
    </form>
  )
}

export default AdminLaptopForm
