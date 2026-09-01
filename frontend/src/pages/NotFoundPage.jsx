import { Link } from 'react-router-dom'
import { Card } from '../components/elements'

function NotFoundPage() {
  return (
    <section className="section">
      <div className="container-app">
        <Card className="mx-auto max-w-xl text-center">
          <p className="status-code">404</p>
          <h1 className="page-title">Halaman tidak ditemukan</h1>
          <p className="mt-3 text-slate-600">
            Alamat yang kamu buka tidak tersedia atau sudah dipindahkan.
          </p>
          <Link className="btn btn-primary mt-6" to="/">
            Kembali ke Beranda
          </Link>
        </Card>
      </div>
    </section>
  )
}

export default NotFoundPage
