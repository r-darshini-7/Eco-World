import type { PropsWithChildren, ReactNode } from 'react'

type AuthLayoutProps = PropsWithChildren<{
  title: string
  subtitle: string
  footer?: ReactNode
}>

export function AuthLayout({ title, subtitle, footer, children }: AuthLayoutProps) {
  return (
    <main className="auth-page">
      <div className="auth-atmosphere">
        <span className="auth-orbit auth-orbit-one" />
        <span className="auth-orbit auth-orbit-two" />
        <span className="auth-grid" />
        <div className="auth-promise">
          <p className="auth-kicker">Darukaa.Earth</p>
          <h2>Make every hectare<br />count.</h2>
          <p>One operational view for the people restoring the living world.</p>
        </div>
      </div>
      <section className="auth-card">
        <div className="mobile-brand">DARUKAA / EARTH</div>
        <h1>{title}</h1>
        <p className="auth-subtitle">{subtitle}</p>
        {children}
        {footer ? <div className="auth-footer">{footer}</div> : null}
      </section>
    </main>
  )
}
