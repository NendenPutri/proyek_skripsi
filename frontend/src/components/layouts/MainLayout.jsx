import { Laptop } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import Navbar from '../fragments/Navbar'

function MainLayout() {
  return (
    <div className="page-shell">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="footer-shell">
        <div className="container-app footer-grid">
          <div className="footer-about">
            <NavLink className="brand-link" to="/">
              <Laptop aria-hidden="true" size={19} />
              LaptopWise
            </NavLink>
            <p className="footer-description">
              Analisis cerdas untuk produktivitas maksimal. Membantu Anda
              menemukan perangkat yang tepat melalui pendekatan data-driven.
            </p>
          </div>
          <div className="footer-links">
            <h2 className="footer-title">Platform</h2>
            <NavLink to="/">Beranda</NavLink>
            <NavLink to="/recommendation">Rekomendasi</NavLink>
            <NavLink to="/laptops">Data Laptop</NavLink>
          </div>
          <div className="footer-links">
            <h2 className="footer-title">Informasi</h2>
            <NavLink to="/about">Tentang Sistem</NavLink>
            <NavLink to="/about">Cara Kerja</NavLink>
            <NavLink to="/about">Informasi Model</NavLink>
          </div>
        </div>
        <div className="footer-bottom">
          (c) 2026 LaptopWise. Analisis cerdas untuk produktivitas maksimal.
        </div>
      </footer>
    </div>
  )
}

export default MainLayout
