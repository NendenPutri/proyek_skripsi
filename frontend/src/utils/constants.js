export const NEED_LABELS = [
  'Administrasi/Perkantoran',
  'Programming',
  'Desain Grafis',
  'Editing Video',
]

export const DEFAULT_ALL_OPTION = 'Semua'

export const DEFAULT_RECOMMENDATION_PAYLOAD = {
  kebutuhan: NEED_LABELS[0],
  budget_maksimal: '',
  ram_min: DEFAULT_ALL_OPTION,
  storage_min: DEFAULT_ALL_OPTION,
  brand: DEFAULT_ALL_OPTION,
  os_family: DEFAULT_ALL_OPTION,
  processor_min_level: DEFAULT_ALL_OPTION,
  gpu_type: 'Tidak wajib',
  touch_screen: DEFAULT_ALL_OPTION,
  jumlah_hasil: 5,
}

export const PROCESSOR_LEVELS = ['Semua', 'Entry', 'Basic', 'Mid', 'High', 'Premium']

export const GPU_OPTIONS = ['Tidak wajib', 'Semua']

export const RAM_MIN_OPTIONS = [DEFAULT_ALL_OPTION, 4, 8, 16, 32]

export const STORAGE_MIN_OPTIONS = [DEFAULT_ALL_OPTION, 128, 256, 512, 1024]

export const TOUCH_SCREEN_OPTIONS = [DEFAULT_ALL_OPTION, 'Ya', 'Tidak']

export const JUMLAH_HASIL_OPTIONS = [5, 10, 15, 20]

export const BUDGET_OPTIONS = [
  { label: 'Semua budget', value: '' },
  { label: 'Maksimal Rp5 juta', value: 5000000 },
  { label: 'Maksimal Rp8 juta', value: 8000000 },
  { label: 'Maksimal Rp12 juta', value: 12000000 },
  { label: 'Maksimal Rp15 juta', value: 15000000 },
  { label: 'Maksimal Rp20 juta', value: 20000000 },
  { label: 'Maksimal Rp30 juta', value: 30000000 },
]

export const FALLBACK_RECOMMENDATION_OPTIONS = {
  kebutuhan: NEED_LABELS,
  budget_options: BUDGET_OPTIONS,
  brand: [DEFAULT_ALL_OPTION],
  processor_level: PROCESSOR_LEVELS,
  ram_min: RAM_MIN_OPTIONS,
  storage_min: STORAGE_MIN_OPTIONS,
  gpu_type: GPU_OPTIONS,
  os_family: [DEFAULT_ALL_OPTION],
  touch_screen: TOUCH_SCREEN_OPTIONS,
  jumlah_hasil: JUMLAH_HASIL_OPTIONS,
}
