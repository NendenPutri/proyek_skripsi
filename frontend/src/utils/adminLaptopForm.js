export const ADMIN_LAPTOP_REQUIRED_FIELDS = [
  'model',
  'brand_name',
  'processor_brand',
  'processor_series',
  'processor_level',
  'ram_class',
  'memory_type',
  'storage_class',
  'gpu_brand',
  'gpu_type',
  'gpu_level',
  'os_family',
  'display_class',
  'resolution_class',
  'touch_screen',
  'warranty_class',
  'price_class',
]

export const ADMIN_LAPTOP_DEFAULT_FORM = {
  model: '',
  brand_name: '',
  price: '',
  price_original: '',
  price_currency: 'IDR',
  price_idr: '',
  rating: '',
  processor: '',
  processor_brand: '',
  processor_series: '',
  processor_score: '',
  processor_level: '',
  ram: '',
  ram_num: '',
  ram_class: '',
  memory_type: '',
  memory_size: '',
  storage_class: '',
  gpu_brand: '',
  gpu_type: '',
  gpu_score: '',
  gpu_level: '',
  os: '',
  os_family: '',
  display_size: '',
  display_class: '',
  resolution_height: '',
  resolution_width: '',
  resolution_class: '',
  touch_screen: '',
  warranty: '',
  warranty_class: '',
  price_class: '',
}

export const ADMIN_LAPTOP_FIELD_GROUPS = [
  {
    title: 'Informasi katalog',
    description: 'Data utama yang akan tampil pada daftar dan detail laptop.',
    fields: [
      { name: 'model', label: 'Model Laptop', required: true },
      { name: 'brand_name', label: 'Brand', type: 'select', optionKey: 'brand', required: true },
      { name: 'rating', label: 'Rating', inputType: 'number', min: 0, max: 5 },
      { name: 'price_idr', label: 'Harga Rupiah', inputType: 'number', min: 0 },
      { name: 'price_original', label: 'Harga Original Dataset', inputType: 'number', min: 0 },
      { name: 'price_currency', label: 'Mata Uang Original' },
      { name: 'price', label: 'Harga Dataset', inputType: 'number', min: 0 },
      {
        name: 'price_class',
        label: 'Kelas Harga',
        type: 'select',
        optionKey: 'price_class',
        required: true,
      },
    ],
  },
  {
    title: 'Processor dan memori',
    description: 'Lengkapi spesifikasi utama yang memengaruhi kecocokan laptop.',
    fields: [
      { name: 'processor', label: 'Processor Lengkap' },
      {
        name: 'processor_brand',
        label: 'Brand Processor',
        type: 'select',
        optionKey: 'processor_brand',
        required: true,
      },
      {
        name: 'processor_series',
        label: 'Series Processor',
        type: 'select',
        optionKey: 'processor_series',
        required: true,
      },
      { name: 'processor_score', label: 'Skor Processor', inputType: 'number', min: 0 },
      {
        name: 'processor_level',
        label: 'Level Processor',
        type: 'select',
        optionKey: 'processor_level',
        required: true,
      },
      { name: 'ram', label: 'RAM Teks' },
      { name: 'ram_num', label: 'RAM Angka', type: 'select', optionKey: 'ram_min' },
      {
        name: 'ram_class',
        label: 'Kelas RAM',
        type: 'select',
        optionKey: 'ram_class',
        required: true,
      },
      {
        name: 'memory_type',
        label: 'Tipe Memori',
        type: 'select',
        optionKey: 'memory_type',
        required: true,
      },
      { name: 'memory_size', label: 'Ukuran Storage', type: 'select', optionKey: 'storage_min' },
      {
        name: 'storage_class',
        label: 'Kelas Storage',
        type: 'select',
        optionKey: 'storage_class',
        required: true,
      },
    ],
  },
  {
    title: 'GPU dan sistem operasi',
    description: 'Pilih informasi grafis dan sistem operasi sesuai spesifikasi laptop.',
    fields: [
      {
        name: 'gpu_brand',
        label: 'Brand GPU',
        type: 'select',
        optionKey: 'gpu_brand',
        required: true,
      },
      { name: 'gpu_type', label: 'Tipe GPU', type: 'select', optionKey: 'gpu_type', required: true },
      { name: 'gpu_score', label: 'Skor GPU', inputType: 'number', min: 0 },
      { name: 'gpu_level', label: 'Level GPU', type: 'select', optionKey: 'gpu_level', required: true },
      { name: 'os', label: 'OS Lengkap' },
      { name: 'os_family', label: 'Keluarga OS', type: 'select', optionKey: 'os_family', required: true },
    ],
  },
  {
    title: 'Display, touchscreen, dan garansi',
    description: 'Lengkapi detail layar, dukungan sentuh, dan informasi garansi.',
    fields: [
      { name: 'display_size', label: 'Ukuran Display', inputType: 'number', min: 0 },
      {
        name: 'display_class',
        label: 'Kelas Display',
        type: 'select',
        optionKey: 'display_class',
        required: true,
      },
      { name: 'resolution_height', label: 'Resolusi Height', inputType: 'number', min: 0 },
      { name: 'resolution_width', label: 'Resolusi Width', inputType: 'number', min: 0 },
      {
        name: 'resolution_class',
        label: 'Kelas Resolusi',
        type: 'select',
        optionKey: 'resolution_class',
        required: true,
      },
      {
        name: 'touch_screen',
        label: 'Touch Screen',
        type: 'select',
        options: [
          { label: 'Yes', value: 'true' },
          { label: 'No', value: 'false' },
        ],
        required: true,
      },
      { name: 'warranty', label: 'Garansi', inputType: 'number', min: 0 },
      {
        name: 'warranty_class',
        label: 'Kelas Garansi',
        type: 'select',
        optionKey: 'warranty_class',
        required: true,
      },
    ],
  },
]

const numericFields = new Set([
  'price',
  'price_original',
  'price_idr',
  'rating',
  'processor_score',
  'ram_num',
  'memory_size',
  'gpu_score',
  'display_size',
  'resolution_height',
  'resolution_width',
  'warranty',
])

const integerFields = new Set([
  'ram_num',
  'memory_size',
  'resolution_height',
  'resolution_width',
  'warranty',
])

function toFormValue(value) {
  if (value === undefined || value === null) {
    return ''
  }

  if (typeof value === 'boolean') {
    return value ? 'true' : 'false'
  }

  return String(value)
}

export function mapLaptopToAdminForm(laptop) {
  return Object.keys(ADMIN_LAPTOP_DEFAULT_FORM).reduce((form, field) => {
    form[field] = toFormValue(laptop?.[field])
    return form
  }, {})
}

function normalizeNumber(value, shouldParseInteger = false) {
  if (value === '') {
    return null
  }

  const numberValue = shouldParseInteger ? Number.parseInt(value, 10) : Number(value)

  return Number.isFinite(numberValue) ? numberValue : null
}

export function serializeAdminLaptopForm(form) {
  const payload = {}

  Object.entries(form).forEach(([field, value]) => {
    if (field === 'touch_screen') {
      payload.touch_screen = value === '' ? null : value === 'true'
      payload.touchscreen_label = value === 'true' ? 'Yes' : 'No'
      return
    }

    if (numericFields.has(field)) {
      payload[field] = normalizeNumber(value, integerFields.has(field))
      return
    }

    const normalizedValue = typeof value === 'string' ? value.trim() : value
    payload[field] = normalizedValue === '' ? null : normalizedValue
  })

  return payload
}

export function validateAdminLaptopForm(form) {
  const errors = {}

  ADMIN_LAPTOP_REQUIRED_FIELDS.forEach((field) => {
    if (form[field] === '') {
      errors[field] = 'Field ini wajib diisi.'
    }
  })

  numericFields.forEach((field) => {
    if (form[field] !== '' && Number(form[field]) < 0) {
      errors[field] = 'Nilai tidak boleh negatif.'
    }
  })

  if (form.rating !== '' && Number(form.rating) > 5) {
    errors.rating = 'Rating maksimal 5.'
  }

  return errors
}
