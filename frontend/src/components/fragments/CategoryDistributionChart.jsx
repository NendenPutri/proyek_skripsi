import { BarChart } from '@mui/x-charts/BarChart'
import { Card, EmptyState, ErrorState, LoadingState } from '../elements'

function normalizeCategoryData(data = []) {
  return data.map((item) => ({
    category: item?.category || '-',
    count: Number.isFinite(Number(item?.count)) ? Number(item.count) : 0,
  }))
}

function CategoryDistributionChart({ data, error, loading, onRetry }) {
  const chartData = normalizeCategoryData(data)
  const hasData = chartData.some((item) => item.count > 0)
  const maxCount = Math.max(...chartData.map((item) => item.count), 1)

  return (
    <Card className="admin-chart-card">
      <div className="admin-chart-heading">
        <div>
          <h3>Distribusi Laptop Berdasarkan Kategori Kebutuhan</h3>
          <p>
            Menampilkan jumlah laptop aktif pada setiap kategori kebutuhan.
          </p>
        </div>
      </div>

      {loading ? <LoadingState message="Memuat statistik kategori..." /> : null}

      {!loading && error ? <ErrorState message={error} onRetry={onRetry} /> : null}

      {!loading && !error && !hasData ? (
        <EmptyState
          description="Belum ada laptop aktif yang dapat dihitung untuk distribusi kategori."
          title="Statistik kategori masih kosong"
        />
      ) : null}

      {!loading && !error && hasData ? (
        <div className="admin-chart-wrap">
          <div className="admin-chart-mobile" aria-label="Distribusi kategori laptop">
            {chartData.map((item) => (
              <div className="admin-chart-mobile-item" key={item.category}>
                <div className="admin-chart-mobile-row">
                  <span>{item.category}</span>
                  <strong>{item.count} laptop</strong>
                </div>
                <progress
                  aria-label={`${item.category}: ${item.count} laptop`}
                  className="admin-chart-progress"
                  max={maxCount}
                  value={item.count}
                />
              </div>
            ))}
          </div>

          <div className="admin-chart-desktop">
            <BarChart
              dataset={chartData}
              height={320}
              layout="horizontal"
              margin={{
                bottom: 32,
                left: 32,
                right: 24,
                top: 24,
              }}
              series={[
                {
                  dataKey: 'count',
                  label: 'Jumlah laptop',
                  valueFormatter: (value) => `${Math.round(value || 0)} laptop`,
                },
              ]}
              xAxis={[
                {
                  min: 0,
                  tickMinStep: 1,
                  valueFormatter: (value) => `${Math.round(value)}`,
                },
              ]}
              yAxis={[
                {
                  dataKey: 'category',
                  scaleType: 'band',
                  width: 155,
                },
              ]}
            />
          </div>
        </div>
      ) : null}
    </Card>
  )
}

export default CategoryDistributionChart
