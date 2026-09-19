import type { PropsWithChildren, ReactNode } from 'react'
import { NavLink } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

type WorkspaceLayoutProps = PropsWithChildren<{
  eyebrow: string
  title: string
  description?: string
  actions?: ReactNode
}>

export function WorkspaceLayout({ eyebrow, title, description, actions, children }: WorkspaceLayoutProps) {
  const { user, logout } = useAuth()
  const initials = user?.full_name
    ?.split(' ')
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase() ?? 'DE'

  return (
    <div className="workspace">
      <aside className="workspace-sidebar">
        <div className="brand-lockup">
          <span className="brand-mark">D</span>
          <div>
            <strong>Darukaa</strong>
            <span>Earth intelligence</span>
          </div>
        </div>
        <nav className="workspace-nav" aria-label="Primary navigation">
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'nav-link nav-link-active' : 'nav-link'}>
            <span className="nav-icon">01</span>Overview
          </NavLink>
          <NavLink to="/projects" className={({ isActive }) => isActive ? 'nav-link nav-link-active' : 'nav-link'}>
            <span className="nav-icon">02</span>Projects
          </NavLink>
        </nav>
        <div className="sidebar-footnote">
          <span className="status-dot" />
          <span>Systems operational</span>
        </div>
      </aside>

      <main className="workspace-main">
        <header className="workspace-topbar">
          <div className="workspace-context">FIELD OPERATIONS / 2026</div>
          <div className="account-menu">
            <span className="account-avatar">{initials}</span>
            <span className="account-name">{user?.full_name ?? 'Workspace admin'}</span>
            <button type="button" className="text-button" onClick={logout}>Sign out</button>
          </div>
        </header>
        <div className="workspace-content">
          <header className="workspace-heading">
            <div>
              <p className="eyebrow">{eyebrow}</p>
              <h1>{title}</h1>
              {description ? <p className="page-description">{description}</p> : null}
            </div>
            {actions ? <div className="heading-actions">{actions}</div> : null}
          </header>
          {children}
        </div>
      </main>
    </div>
  )
}
