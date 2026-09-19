import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import type { AnalyticsOverview } from '../types/dashboard'
import { WorkspaceLayout } from '../components/WorkspaceLayout'

export function DashboardPage() {
  const { user } = useAuth()
  const [metrics, setMetrics] = useState<AnalyticsOverview | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const response = await api.get<AnalyticsOverview>('/analytics/overview')
        setMetrics(response.data)
      } catch (error) {
        setError('Analytics are temporarily unavailable.')
        console.error('Failed to load dashboard metrics', error)
      }
    }

    void loadMetrics()
  }, [])

  const statusBreakdown = metrics?.project_status_breakdown ?? {}
  const hasProjects = (metrics?.total_projects ?? 0) > 0
  const totalBudget = metrics?.total_budget ?? 0
  const compactBudget = totalBudget >= 1_000_000
    ? `$${(totalBudget / 1_000_000).toFixed(1)}m`
    : `$${(totalBudget / 1_000).toFixed(0)}k`

  return (
    <WorkspaceLayout
      eyebrow="Command center"
      title="Operational overview"
      description={`A live read on ${user?.full_name?.split(' ')[0] ?? 'your'} restoration portfolio.`}
      actions={<Link to="/projects" className="primary-button">Open portfolio <span>↗</span></Link>}
    >
      {error ? <div className="notice notice-error">{error}</div> : null}
      <section className="metrics-grid">
        <article className="metric-panel metric-panel-accent"><span>Portfolio projects</span><strong>{metrics?.total_projects ?? 0}</strong><small>Tracked initiatives</small></article>
        <article className="metric-panel"><span>Sites monitored</span><strong>{metrics?.sites_monitored ?? 0}</strong><small>Across all projects</small></article>
        <article className="metric-panel"><span>Active projects</span><strong>{metrics?.active_projects ?? 0}</strong><small>Currently in motion</small></article>
        <article className="metric-panel"><span>Committed budget</span><strong>{compactBudget}</strong><small>${totalBudget.toLocaleString()} total</small></article>
      </section>

      {!hasProjects ? (
        <section className="empty-state dashboard-empty">
          <div className="empty-number">01</div>
          <div>
            <p className="eyebrow">First signal</p>
            <h2>Your portfolio is ready for its first project.</h2>
            <p>Create a project, add its field sites, and the operational picture will appear here.</p>
            <Link to="/projects" className="primary-button">Create a project <span>→</span></Link>
          </div>
        </section>
      ) : (
        <section className="dashboard-lower-grid">
          <article className="dashboard-panel">
            <div className="panel-title-row"><div><p className="eyebrow">Portfolio pulse</p><h2>Project status</h2></div><Link to="/projects" className="inline-link">View all</Link></div>
            <div className="status-list">
              {['active', 'draft', 'paused', 'completed'].map((status) => <div className="status-row" key={status}><span>{status}</span><strong>{statusBreakdown[status] ?? 0}</strong><i style={{ width: `${Math.min(100, ((statusBreakdown[status] ?? 0) / (metrics?.total_projects || 1)) * 100)}%` }} /></div>)}
            </div>
          </article>
          <article className="dashboard-panel signal-panel"><p className="eyebrow">Field signal</p><h2>Keep the map current.</h2><p>Sites with fresh coordinates and geometry produce the clearest picture of restoration progress.</p><Link to="/projects" className="inline-link">Review field sites →</Link></article>
        </section>
      )}
    </WorkspaceLayout>
  )
}
