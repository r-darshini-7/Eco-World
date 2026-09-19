import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../services/api'
import type { Project } from '../types/project'
import { WorkspaceLayout } from '../components/WorkspaceLayout'

type ProjectDraft = {
  name: string
  country: string
  status: Project['status']
  budget: number
  description: string
}

const emptyDraft: ProjectDraft = {
  name: '',
  country: '',
  status: 'draft',
  budget: 0,
  description: '',
}

export function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [draft, setDraft] = useState<ProjectDraft>(emptyDraft)

  const loadProjects = async () => {
    try {
      const response = await api.get<Project[]>('/projects')
      setProjects(response.data)
      setError('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load projects.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadProjects()
  }, [])

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      await api.post('/projects', {
        ...draft,
        budget: Number(draft.budget),
      })
      setDraft(emptyDraft)
      await loadProjects()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create project.')
    }
  }

  return (
    <WorkspaceLayout eyebrow="Portfolio registry" title="Projects" description="Organize restoration work, field sites, and the capital behind them.">
      <section className="portfolio-layout">
        <div className="panel-card form-panel">
          <div className="panel-title-row"><div><p className="eyebrow">New record</p><h2>Create project</h2></div><span className="panel-index">01</span></div>
          <form className="stacked-form" onSubmit={handleSubmit}>
            <label>
              <span>Name</span>
              <input value={draft.name} onChange={(event) => setDraft({ ...draft, name: event.target.value })} required />
            </label>
            <label>
              <span>Country</span>
              <input value={draft.country} onChange={(event) => setDraft({ ...draft, country: event.target.value })} required />
            </label>
            <div className="two-column">
              <label>
                <span>Status</span>
                <select value={draft.status} onChange={(event) => setDraft({ ...draft, status: event.target.value as Project['status'] })}>
                  <option value="draft">Draft</option>
                  <option value="active">Active</option>
                  <option value="paused">Paused</option>
                  <option value="completed">Completed</option>
                </select>
              </label>
              <label>
                <span>Budget</span>
                <input type="number" min="0" step="1000" value={draft.budget} onChange={(event) => setDraft({ ...draft, budget: Number(event.target.value) })} />
              </label>
            </div>
            <label>
              <span>Description</span>
              <textarea value={draft.description} onChange={(event) => setDraft({ ...draft, description: event.target.value })} rows={4} />
            </label>
            {error ? <p className="form-error">{error}</p> : null}
            <button className="primary-button" type="submit">Save project <span>→</span></button>
          </form>
        </div>

        <div className="portfolio-list">
          <div className="list-heading"><div><p className="eyebrow">Active registry</p><h2>All projects</h2></div><span className="count-chip">{projects.length.toString().padStart(2, '0')} records</span></div>
          {loading ? <div className="loading-card">Loading portfolio records<span className="loading-line" /></div> : null}
          {!loading && projects.length === 0 ? <div className="empty-state compact-empty"><div className="empty-number">00</div><div><h2>No projects yet.</h2><p>Use the form to create your first restoration initiative.</p></div></div> : null}
          <div className="card-grid">
            {projects.map((project) => (
              <Link key={project.id} to={`/projects/${project.id}`} className="project-card">
                <div className="project-card-header">
                  <div><span className="card-kicker">PRJ-{String(project.id).padStart(4, '0')}</span><strong>{project.name}</strong></div>
                  <span className="status-badge">{project.status}</span>
                </div>
                <p className="project-location"><span className="location-pin">+</span>{project.country}</p>
                <div className="project-card-meta"><span><b>{project.site_count}</b> sites</span><span><b>${(project.budget / 1000).toFixed(0)}k</b> budget</span></div>
                <span className="card-arrow">↗</span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </WorkspaceLayout>
  )
}
