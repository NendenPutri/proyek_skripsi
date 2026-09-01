import { Info } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import {
  Button,
  EmptyState,
  ErrorState,
  Input,
  LoadingState,
  Select,
} from '../components/elements'
import { LaptopCard } from '../components/fragments'
import useOptions from '../hooks/useOptions'
import { getLaptops } from '../services/laptopService'
import { DEFAULT_ALL_OPTION, FALLBACK_RECOMMENDATION_OPTIONS } from '../utils/constants'

const initialFilters = {
  search: '',
  brand: DEFAULT_ALL_OPTION,
  kebutuhan: DEFAULT_ALL_OPTION,
  limit: 12,
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

function withAllOption(optionList) {
  const hasAllOption = optionList.some((option) => getOptionValue(option) === DEFAULT_ALL_OPTION)

  return hasAllOption ? optionList : [DEFAULT_ALL_OPTION, ...optionList]
}

function resolveLaptopList(response) {
  const data = response?.data ?? response

  if (Array.isArray(data)) {
    return data
  }

  return data?.laptops || data?.items || data?.results || []
}

function buildLaptopParams(filters) {
  return {
    limit: filters.limit,
    search: filters.search,
    brand: filters.brand === DEFAULT_ALL_OPTION ? '' : filters.brand,
    kebutuhan: filters.kebutuhan === DEFAULT_ALL_OPTION ? '' : filters.kebutuhan,
  }
}

function LaptopsPage() {
  const { options, error: optionsError } = useOptions()
  const [filters, setFilters] = useState(initialFilters)
  const [appliedFilters, setAppliedFilters] = useState(initialFilters)
  const [refreshKey, setRefreshKey] = useState(0)
  const [laptops, setLaptops] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const filterOptions = useMemo(
    () => ({
      brand: withAllOption(getOptionList(options, 'brand')),
      kebutuhan: withAllOption(getOptionList(options, 'kebutuhan')),
      limit: [6, 12, 24, 48],
    }),
    [options],
  )

  useEffect(() => {
    let isMounted = true

    async function fetchLaptops() {
      try {
        const response = await getLaptops(buildLaptopParams(appliedFilters))

        if (isMounted) {
          setLaptops(resolveLaptopList(response))
          setError('')
        }
      } catch (requestError) {
        if (isMounted) {
          setLaptops([])
          setError(
            requestError?.message
              ? `Gagal memuat data laptop: ${requestError.message}`
              : 'Gagal memuat data laptop. Pastikan layanan aplikasi sedang aktif.',
          )
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchLaptops()

    return () => {
      isMounted = false
    }
  }, [appliedFilters, refreshKey])

  function handleChange(event) {
    const { name, value } = event.target

    setFilters((currentFilters) => ({
      ...currentFilters,
      [name]: name === 'limit' ? Number(value) : value,
    }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setAppliedFilters(filters)
  }

  function handleRetry() {
    setLoading(true)
    setRefreshKey((currentKey) => currentKey + 1)
  }

  return (
    <section className="laptops-page">
      <div className="container-app">
        <header className="laptops-header">
          <p className="laptops-eyebrow">Data Laptop</p>
          <h1 className="laptops-title">
            Daftar <span className="hero-highlight">Laptop</span>{" "}
          </h1>
          <p className="laptops-description">
            Lihat data laptop yang digunakan oleh sistem rekomendasi. Data ini
            berasal dari hasil preprocessing dan digunakan sebagai dasar
            rekomendasi.
          </p>
        </header>

        <form className="laptops-filter-panel" onSubmit={handleSubmit}>
          <div className="laptops-filter-grid">
            <Input
              label="Cari"
              name="search"
              onChange={handleChange}
              placeholder="Model atau brand"
              value={filters.search}
            />
            <Select
              label="Brand"
              name="brand"
              onChange={handleChange}
              options={filterOptions.brand}
              value={filters.brand}
            />
            <Select
              label="Kebutuhan"
              name="kebutuhan"
              onChange={handleChange}
              options={filterOptions.kebutuhan}
              value={filters.kebutuhan}
            />
            <Select
              label="Limit"
              name="limit"
              onChange={handleChange}
              options={filterOptions.limit}
              value={filters.limit}
            />
          </div>
          <div className="laptops-filter-actions">
            <Button
              className="laptops-filter-button"
              disabled={loading}
              type="submit"
            >
              Terapkan Filter
            </Button>
          </div>
        </form>

        <div className="laptops-note">
          <Info aria-hidden="true" size={20} />
          <p>
            Harga laptop ditampilkan dalam Rupiah berdasarkan hasil konversi
            pada tahap preprocessing dataset. Sistem tidak melakukan pembelian
            laptop dan tidak mengambil data marketplace secara otomatis.
          </p>
        </div>

        {optionsError ? (
          <p className="laptops-options-note">{optionsError}</p>
        ) : null}

        {loading ? <LoadingState message="Memuat data laptop..." /> : null}
        {!loading && error ? (
          <ErrorState message={error} onRetry={handleRetry} />
        ) : null}
        {!loading && !error && !laptops.length ? (
          <EmptyState
            description="Coba ubah keyword, brand, kebutuhan, atau limit pencarian."
            title="Data laptop tidak ditemukan"
          />
        ) : null}
        {!loading && !error && laptops.length ? (
          <div className="laptops-grid">
            {laptops.map((laptop, index) => (
              <LaptopCard
                key={laptop.id || laptop.model || index}
                laptop={laptop}
                variant="catalog"
              />
            ))}
          </div>
        ) : null}
      </div>
    </section>
  );
}

export default LaptopsPage
