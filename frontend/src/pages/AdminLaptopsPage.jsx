import { Plus } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button, ConfirmDialog, EmptyState, ErrorState, Input, LoadingState, Notification, Select } from '../components/elements'
import { AdminLaptopTable } from '../components/fragments'
import useAdminLaptops from '../hooks/useAdminLaptops'
import useDebouncedValue from '../hooks/useDebouncedValue'
import { deleteAdminLaptop } from '../services/adminLaptopService'
import { NEED_LABELS } from '../utils/constants'

const limitOptions = [10, 20, 50, 100]
const statusOptions = [
  { label: 'Semua status', value: 'all' },
  { label: 'Aktif', value: 'active' },
  { label: 'Nonaktif', value: 'inactive' },
]
const sourceOptions = [
  { label: 'Semua sumber', value: '' },
  { label: 'Admin', value: 'admin' },
]

function AdminLaptopsPage() {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('all')
  const [source, setSource] = useState('')
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(20)
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState('desc')
  const [selectedLaptop, setSelectedLaptop] = useState(null)
  const [deleting, setDeleting] = useState(false)
  const [notification, setNotification] = useState(null)
  const debouncedSearch = useDebouncedValue(search, 450)

  const queryParams = useMemo(
    () => ({
      category,
      limit,
      page,
      search: debouncedSearch,
      sort_by: sortBy,
      sort_order: sortOrder,
      source,
      status,
    }),
    [category, debouncedSearch, limit, page, sortBy, sortOrder, source, status],
  )

  const { error, items, loading, pagination, refetch } = useAdminLaptops(queryParams)

  function resetPage() {
    setPage(1)
  }

  function handleSort(column) {
    if (sortBy === column) {
      setSortOrder((currentOrder) => (currentOrder === 'asc' ? 'desc' : 'asc'))
      return
    }

    setSortBy(column)
    setSortOrder('asc')
  }

  async function handleDeactivate() {
    if (!selectedLaptop) {
      return
    }

    setDeleting(true)

    try {
      await deleteAdminLaptop(selectedLaptop.id)
      setNotification({
        message: 'Laptop berhasil dinonaktifkan.',
        type: 'success',
      })
      setSelectedLaptop(null)
      await refetch()
    } catch (requestError) {
      setNotification({
        message: requestError?.message || 'Laptop gagal dinonaktifkan.',
        type: 'error',
      })
    } finally {
      setDeleting(false)
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
          <p className="admin-section-eyebrow">Data Laptop Admin</p>
          <h2 className="admin-page-title">Kelola Laptop</h2>
          <p className="admin-page-description">
            Kelola katalog laptop yang tersedia untuk pengguna. Laptop yang dinonaktifkan
            tidak akan muncul di halaman publik.
          </p>
        </div>
        <Link className="btn btn-primary" to="/admin/laptops/create">
          <Plus aria-hidden="true" size={16} />
          Tambah Laptop
        </Link>
      </section>

      <section className="admin-filter-card">
        <Input
          label="Search"
          name="search"
          onChange={(event) => {
            setSearch(event.target.value)
            resetPage()
          }}
          placeholder="Cari model atau brand"
          value={search}
        />
        <Select
          label="Kategori Prediksi"
          name="category"
          onChange={(event) => {
            setCategory(event.target.value)
            resetPage()
          }}
          options={[
            { label: 'Semua kategori', value: '' },
            ...NEED_LABELS.map((label) => ({ label, value: label })),
          ]}
          value={category}
        />
        <Select
          label="Status"
          name="status"
          onChange={(event) => {
            setStatus(event.target.value)
            resetPage()
          }}
          options={statusOptions}
          value={status}
        />
        <Select
          label="Sumber Data"
          name="source"
          onChange={(event) => {
            setSource(event.target.value)
            resetPage()
          }}
          options={sourceOptions}
          value={source}
        />
        <Select
          label="Limit"
          name="limit"
          onChange={(event) => {
            setLimit(Number(event.target.value))
            resetPage()
          }}
          options={limitOptions}
          value={limit}
        />
      </section>

      {loading ? <LoadingState message="Memuat data laptop admin..." /> : null}

      {!loading && error ? <ErrorState message={error} onRetry={refetch} /> : null}

      {!loading && !error && items.length === 0 ? (
        <EmptyState
          action={<Link className="btn btn-primary" to="/admin/laptops/create">Tambah laptop manual</Link>}
          description="Belum ada data yang cocok dengan filter saat ini."
          title="Data laptop admin kosong"
        />
      ) : null}

      {!loading && !error && items.length > 0 ? (
        <>
          <AdminLaptopTable
            items={items}
            onDeactivate={setSelectedLaptop}
            onSort={handleSort}
            sortBy={sortBy}
            sortOrder={sortOrder}
          />

          <div className="admin-pagination">
            <p>
              Total {pagination?.total || 0} data, halaman {pagination?.page || page} dari{' '}
              {pagination?.total_pages || 1}
            </p>
            <div className="admin-pagination-actions">
              <Button
                disabled={page <= 1}
                onClick={() => setPage((currentPage) => Math.max(1, currentPage - 1))}
                variant="secondary"
              >
                Sebelumnya
              </Button>
              <Button
                disabled={!pagination?.total_pages || page >= pagination.total_pages}
                onClick={() => setPage((currentPage) => currentPage + 1)}
                variant="secondary"
              >
                Berikutnya
              </Button>
            </div>
          </div>
        </>
      ) : null}

      {selectedLaptop ? (
        <ConfirmDialog
          confirmLabel="Nonaktifkan"
          description={`Laptop "${selectedLaptop.model}" akan dinonaktifkan. Data tidak dihapus permanen.`}
          loading={deleting}
          onCancel={() => setSelectedLaptop(null)}
          onConfirm={handleDeactivate}
          title="Nonaktifkan laptop?"
        />
      ) : null}
    </div>
  )
}

export default AdminLaptopsPage
