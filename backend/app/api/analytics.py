from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.project import Project, Site
from app.schemas.analytics import AnalyticsOverview

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/overview', response_model=AnalyticsOverview)
def analytics_overview(
    current_user: dict[str, str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    projects = db.scalars(select(Project)).all()
    sites = db.scalars(select(Site)).all()

    status_breakdown = Counter(project.status for project in projects)
    active_count = sum(1 for project in projects if project.status == 'active')

    return {
        'total_projects': len(projects),
        'active_projects': active_count,
        'sites_monitored': len(sites),
        'total_budget': sum(float(project.budget) for project in projects),
        'project_status_breakdown': dict(status_breakdown),
    }
