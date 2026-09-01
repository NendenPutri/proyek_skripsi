import { LayoutDashboard, Laptop, LogOut, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { Button, ConfirmDialog } from '../elements'
import { useAuth } from '../../hooks/useAuth'

const adminNavigation = [
  { label: 'Dashboard', to: '/admin', icon: LayoutDashboard, end: true },
  { label: 'Data Laptop', to: '/admin/laptops', icon: Laptop },
]

function getAdminNavClass({ isActive }) {
  return `admin-nav-link ${isActive ? 'admin-nav-link-active' : ''}`.trim()
}

function AdminLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [isLogoutDialogOpen, setIsLogoutDialogOpen] = useState(false)
  const { admin, logout } = useAuth()

  function closeSidebar() {
    setIsSidebarOpen(false)
  }

  function handleLogoutConfirm() {
    setIsLogoutDialogOpen(false)
    logout()
  }

  return (
    <div className="admin-shell">
      <aside className={`admin-sidebar ${isSidebarOpen ? 'admin-sidebar-open' : ''}`}>
        <div className="admin-sidebar-brand">
          <NavLink className="brand-link" onClick={closeSidebar} to="/admin">
            <Laptop aria-hidden="true" size={20} />
            LaptopWise Admin
          </NavLink>
          <button
            aria-label="Tutup menu admin"
            className="admin-icon-button lg:hidden"
            onClick={closeSidebar}
            type="button"
          >
            <X aria-hidden="true" size={20} />
          </button>
        </div>

        <nav className="admin-nav" aria-label="Navigasi admin">
          {adminNavigation.map((item) => {
            const Icon = item.icon

            return (
              <NavLink
                className={getAdminNavClass}
                end={item.end}
                key={item.to}
                onClick={closeSidebar}
                to={item.to}
              >
                <Icon aria-hidden="true" size={18} />
                {item.label}
              </NavLink>
            )
          })}
        </nav>

        <div className="admin-sidebar-footer">
          <p className="admin-sidebar-label">Login sebagai</p>
          <p className="admin-sidebar-name">{admin?.name || 'Admin'}</p>
          <p className="admin-sidebar-email">{admin?.email || '-'}</p>
        </div>
      </aside>

      {isSidebarOpen ? (
        <button
          aria-label="Tutup overlay menu admin"
          className="admin-sidebar-backdrop"
          onClick={closeSidebar}
          type="button"
        />
      ) : null}

      <div className="admin-main">
        <header className="admin-header">
          <button
            aria-label="Buka menu admin"
            className="admin-icon-button lg:hidden"
            onClick={() => setIsSidebarOpen(true)}
            type="button"
          >
            <Menu aria-hidden="true" size={20} />
          </button>
          <div>
            <p className="admin-header-eyebrow">Area Admin</p>
            <h1 className="admin-header-title">LaptopWise Admin</h1>
          </div>
          <Button
            className="admin-logout-button"
            onClick={() => setIsLogoutDialogOpen(true)}
            variant="ghost"
          >
            <LogOut aria-hidden="true" size={16} />
            Logout
          </Button>
        </header>

        <main className="admin-content">
          <Outlet />
        </main>
      </div>

      {isLogoutDialogOpen ? (
        <ConfirmDialog
          confirmLabel="Logout"
          description="Anda akan keluar dari area admin. Pastikan pekerjaan yang sedang dilakukan sudah disimpan."
          onCancel={() => setIsLogoutDialogOpen(false)}
          onConfirm={handleLogoutConfirm}
          title="Keluar dari akun admin?"
        />
      ) : null}
    </div>
  )
}

export default AdminLayout
