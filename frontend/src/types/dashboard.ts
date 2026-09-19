export type AnalyticsOverview = {
  total_projects: number
  active_projects: number
  sites_monitored: number
  total_budget: number
  project_status_breakdown: Record<string, number>
}
