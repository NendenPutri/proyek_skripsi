import { Laptop, Menu, ShieldCheck, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink } from 'react-router-dom'

const navigationItems = [
  { label: 'Beranda', to: '/' },
  { label: 'Rekomendasi', to: '/recommendation' },
  { label: 'Data Laptop', to: '/laptops' },
  { label: 'Tentang Sistem', to: '/about' },
]

function getNavLinkClass({ isActive }) {
  return `navbar-link ${isActive ? 'navbar-link-active' : ''}`.trim()
}

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  function closeMenu() {
    setIsMenuOpen(false)
  }

  function toggleMenu() {
    setIsMenuOpen((currentState) => !currentState)
  }

  return (
    <header className="navbar-shell">
      <nav className="navbar-inner">
        <NavLink className="brand-link" onClick={closeMenu} to="/">
          <Laptop aria-hidden="true" size={19} />
          LaptopWise
        </NavLink>

        <div className="navbar-links" aria-label="Navigasi utama">
          {navigationItems.map((item) => (
            <NavLink className={getNavLinkClass} key={item.to} to={item.to}>
              {item.label}
            </NavLink>
          ))}
        </div>

        <div className="navbar-actions">
          <NavLink className="navbar-admin-link" to="/admin/login">
            <ShieldCheck aria-hidden="true" size={14} />
            Admin
          </NavLink>
          <NavLink className="navbar-cta" to="/recommendation">
            Mulai Rekomendasi
          </NavLink>
        </div>
        <button
          aria-controls="mobile-navigation"
          aria-expanded={isMenuOpen}
          aria-label={isMenuOpen ? 'Tutup navigasi' : 'Buka navigasi'}
          className="navbar-menu-button"
          onClick={toggleMenu}
          type="button"
        >
          {isMenuOpen ? <X aria-hidden="true" size={22} /> : <Menu aria-hidden="true" size={22} />}
        </button>
      </nav>

      <div
        className={`mobile-nav-panel ${isMenuOpen ? 'mobile-nav-panel-open' : ''}`}
        id="mobile-navigation"
      >
        <div className="mobile-nav-links" aria-label="Navigasi mobile">
          {navigationItems.map((item) => (
            <NavLink
              className={getNavLinkClass}
              key={item.to}
              onClick={closeMenu}
              to={item.to}
            >
              {item.label}
            </NavLink>
          ))}
        </div>

        <div className="mobile-nav-actions">
          <NavLink className="mobile-nav-admin" onClick={closeMenu} to="/admin/login">
            <ShieldCheck aria-hidden="true" size={18} />
            Login Admin
          </NavLink>
          <NavLink className="mobile-nav-cta" onClick={closeMenu} to="/recommendation">
            Mulai Rekomendasi
          </NavLink>
        </div>
      </div>
    </header>
  )
}

export default Navbar
