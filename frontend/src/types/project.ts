export type ProjectStatus = 'draft' | 'active' | 'paused' | 'completed'
export type SiteStatus = 'planned' | 'monitoring' | 'flagged' | 'resolved'

export type Project = {
  id: number
  name: string
  country: string
  status: ProjectStatus
  budget: number
  description?: string | null
  site_count: number
}

export type Site = {
  id: number
  project_id: number
  name: string
  status: SiteStatus
  latitude?: number | null
  longitude?: number | null
  note?: string | null
}

export type Geometry = {
  type: string
  coordinates: unknown[]
}

export type SiteDetails = Site & {
  geometry?: Geometry | null
}
