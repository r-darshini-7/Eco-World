from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_projects: int
    active_projects: int
    sites_monitored: int
    total_budget: float
    project_status_breakdown: dict[str, int]
