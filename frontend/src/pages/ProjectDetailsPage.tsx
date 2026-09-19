import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { api } from '../services/api'
import type { Geometry, Project, Site, SiteDetails } from '../types/project'
import { WorkspaceLayout } from '../components/WorkspaceLayout'

type SiteDraft = {
  name: string
  status: Site['status']
  latitude: string
  longitude: string
  note: string
}

const emptyDraft: SiteDraft = {
  name: '',
  status: 'planned',
  latitude: '',
  longitude: '',
  note: '',
}

export function ProjectDetailsPage() {
  const { projectId } = useParams()
  const [project, setProject] = useState<Project | null>(null)
  const [sites, setSites] = useState<Site[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [draft, setDraft] = useState<SiteDraft>(emptyDraft)
  const [selectedSite, setSelectedSite] = useState<SiteDetails | null>(null)
  const [geometryText, setGeometryText] = useState('')
  const [geometryError, setGeometryError] = useState('')
  const [geometrySaving, setGeometrySaving] = useState(false)

  const loadProjectData = async () => {
    if (!projectId) return
    try {
      const [projectResponse, sitesResponse] = await Promise.all([
        api.get<Project>(`/projects/${projectId}`),
        api.get<Site[]>(`/projects/${projectId}/sites`),
      ])
      setProject(projectResponse.data)
      setSites(sitesResponse.data)
      setError('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load project details.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadProjectData()
  }, [projectId])

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!projectId) return

    try {
      await api.post(`/projects/${projectId}/sites`, {
        ...draft,
        latitude: draft.latitude === '' ? null : Number(draft.latitude),
        longitude: draft.longitude === '' ? null : Number(draft.longitude),
      })
      setDraft(emptyDraft)
      await loadProjectData()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create site.')
    }
  }

  const selectSite = async (site: Site) => {
    setGeometryError('')
    try {
      const response = await api.get<SiteDetails>(`/sites/${site.id}`)
      setSelectedSite(response.data)
      setGeometryText(response.data.geometry ? JSON.stringify(response.data.geometry, null, 2) : '')
    } catch (err) {
      setGeometryError(err instanceof Error ? err.message : 'Unable to load site geometry.')
    }
  }

  const saveGeometry = async () => {
    if (!selectedSite) return

    try {
      const geometry = JSON.parse(geometryText) as Geometry
      if (!geometry.type || !Array.isArray(geometry.coordinates)) {
        throw new Error('Geometry must include a type and coordinates array.')
      }
      setGeometrySaving(true)
      setGeometryError('')
      await api.post(`/sites/${selectedSite.id}/geometry`, geometry)
      setSelectedSite({ ...selectedSite, geometry })
      setGeometryText(JSON.stringify(geometry, null, 2))
    } catch (err) {
      setGeometryError(err instanceof Error ? err.message : 'Enter valid GeoJSON geometry.')
    } finally {
      setGeometrySaving(false)
    }
  }

  if (loading) {
    return <main className="page-shell"><p>Loading project details…</p></main>
  }

  if (!project) {
    return (
      <main className="page-shell">
        <p>Project not found.</p>
        <Link to="/projects" className="secondary-link">Back to projects</Link>
      </main>
    )
  }

  return (
    <WorkspaceLayout eyebrow="Project dossier" title={project.name} description={project.description || 'Field operations and site intelligence for this restoration project.'} actions={<Link to="/projects" className="secondary-button">← All projects</Link>}>
      <section className="project-overview panel-card project-overview-grid">
        <div><span className="overview-label">Country</span><strong>{project.country}</strong></div>
        <div><span className="overview-label">Status</span><strong className="overview-status">{project.status}</strong></div>
        <div><span className="overview-label">Budget</span><strong>${project.budget.toLocaleString()}</strong></div>
        <div><span className="overview-label">Field sites</span><strong>{sites.length.toString().padStart(2, '0')}</strong></div>
      </section>

      <section className="panel-grid">
        <div className="panel-card form-panel">
          <div className="panel-title-row"><div><p className="eyebrow">Field register</p><h2>Add site</h2></div><span className="panel-index">02</span></div>
          <form className="stacked-form" onSubmit={handleSubmit}>
            <label>
              <span>Name</span>
              <input value={draft.name} onChange={(event) => setDraft({ ...draft, name: event.target.value })} required />
            </label>
            <div className="two-column">
              <label>
                <span>Status</span>
                <select value={draft.status} onChange={(event) => setDraft({ ...draft, status: event.target.value as Site['status'] })}>
                  <option value="planned">Planned</option>
                  <option value="monitoring">Monitoring</option>
                  <option value="flagged">Flagged</option>
                  <option value="resolved">Resolved</option>
                </select>
              </label>
            </div>
            <div className="two-column">
              <label>
                <span>Latitude</span>
                <input type="number" step="0.0001" value={draft.latitude} onChange={(event) => setDraft({ ...draft, latitude: event.target.value })} />
              </label>
              <label>
                <span>Longitude</span>
                <input type="number" step="0.0001" value={draft.longitude} onChange={(event) => setDraft({ ...draft, longitude: event.target.value })} />
              </label>
            </div>
            <label>
              <span>Notes</span>
              <textarea rows={3} value={draft.note} onChange={(event) => setDraft({ ...draft, note: event.target.value })} />
            </label>
            {error ? <p className="form-error">{error}</p> : null}
            <button type="submit">Add site</button>
          </form>
        </div>

        <div className="panel-card sites-panel">
          <div className="panel-title-row"><div><p className="eyebrow">Field register</p><h2>Sites</h2></div><span className="count-chip">{sites.length.toString().padStart(2, '0')} sites</span></div>
          {sites.length === 0 ? <p>No sites added yet.</p> : null}
          <div className="site-list">
            {sites.map((site) => (
                <article key={site.id} className={`site-item${selectedSite?.id === site.id ? ' site-item-selected' : ''}`}>
                <div className="project-card-header">
                  <strong>{site.name}</strong>
                  <span className="status-badge">{site.status}</span>
                </div>
                <p>
                  {site.latitude != null && site.longitude != null
                    ? `${site.latitude}, ${site.longitude}`
                    : 'Coordinates pending'}
                </p>
                <small>{site.note || 'No notes yet.'}</small>
                <button type="button" className="site-select-button" onClick={() => void selectSite(site)}>
                  {selectedSite?.id === site.id ? 'Selected for mapping' : 'Edit geometry'}
                </button>
              </article>
            ))}
          </div>
        </div>
      </section>

      {selectedSite ? (
        <section className="geometry-panel panel-card">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Site geometry</p>
              <h2>{selectedSite.name}</h2>
            </div>
            <span className="geometry-format">GeoJSON</span>
          </div>
          <div className="geometry-editor-grid">
            <label>
              <span>Geometry payload</span>
              <textarea
                className="geometry-input"
                rows={10}
                value={geometryText}
                onChange={(event) => setGeometryText(event.target.value)}
                placeholder={'{\n  "type": "Polygon",\n  "coordinates": []\n}'}
              />
            </label>
            <div className="geometry-preview" aria-label="Geometry preview">
              <span className="preview-label">Preview</span>
              {selectedSite.geometry ? <GeometryPreview geometry={selectedSite.geometry} /> : <p>No geometry saved yet.</p>}
            </div>
          </div>
          {geometryError ? <p className="form-error">{geometryError}</p> : null}
          <button type="button" onClick={() => void saveGeometry()} disabled={geometrySaving}>
            {geometrySaving ? 'Saving geometry…' : 'Save geometry'}
          </button>
        </section>
      ) : null}
    </WorkspaceLayout>
  )
}

function GeometryPreview({ geometry }: { geometry: Geometry }) {
  const ring = geometry.type === 'Polygon' && Array.isArray(geometry.coordinates[0])
    ? geometry.coordinates[0] as number[][]
    : []
  const longitudes = ring.map(([longitude]) => longitude)
  const latitudes = ring.map(([, latitude]) => latitude)
  const minLongitude = Math.min(...longitudes)
  const maxLongitude = Math.max(...longitudes)
  const minLatitude = Math.min(...latitudes)
  const maxLatitude = Math.max(...latitudes)
  const longitudeRange = maxLongitude - minLongitude || 1
  const latitudeRange = maxLatitude - minLatitude || 1
  const points = ring.map(([longitude, latitude]) => {
    const x = 12 + ((longitude - minLongitude) / longitudeRange) * 76
    const y = 68 - ((latitude - minLatitude) / latitudeRange) * 56
    return `${x},${y}`
  })

  return (
    <div className="geometry-visual">
      <svg viewBox="0 0 100 80" role="img" aria-label={`${geometry.type} geometry`}>
        <path d={points.length > 1 ? `M ${points.join(' L ')} Z` : 'M 16 40 L 50 16 L 84 40 L 50 64 Z'} />
      </svg>
      <strong>{geometry.type}</strong>
      <small>{ring.length ? `${ring.length} coordinate points` : 'Saved geometry'}</small>
    </div>
  )
}
