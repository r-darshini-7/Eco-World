from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_roles
from app.db.session import get_db
from app.models.project import Project, Site
from app.schemas.projects import ProjectCreate, ProjectRead, SiteCreate, SiteRead

router = APIRouter(prefix='/projects', tags=['projects'])


@router.post('', response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    current_user: dict[str, str] = Depends(require_roles('ADMIN')),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    project = Project(
        name=payload.name,
        country=payload.country,
        status=payload.status,
        budget=float(payload.budget),
        description=payload.description,
        created_by=None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {
        'id': project.id,
        'name': project.name,
        'country': project.country,
        'status': project.status,
        'budget': project.budget,
        'description': project.description,
        'site_count': 0,
    }


@router.get('', response_model=list[ProjectRead])
def list_projects(
    current_user: dict[str, str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict[str, object]]:
    projects = db.scalars(select(Project)).all()
    return [
        {
            'id': project.id,
            'name': project.name,
            'country': project.country,
            'status': project.status,
            'budget': project.budget,
            'description': project.description,
            'site_count': len(project.sites),
        }
        for project in projects
    ]


@router.get('/{project_id}', response_model=ProjectRead)
def get_project(
    project_id: int,
    current_user: dict[str, str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return {
        'id': project.id,
        'name': project.name,
        'country': project.country,
        'status': project.status,
        'budget': project.budget,
        'description': project.description,
        'site_count': len(project.sites),
    }


@router.post('/{project_id}/sites', response_model=SiteRead, status_code=status.HTTP_201_CREATED)
def create_site_for_project(
    project_id: int,
    payload: SiteCreate,
    current_user: dict[str, str] = Depends(require_roles('ADMIN')),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')

    site = Site(
        project_id=project_id,
        name=payload.name,
        status=payload.status,
        latitude=payload.latitude,
        longitude=payload.longitude,
        note=payload.note,
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return {
        'id': site.id,
        'project_id': site.project_id,
        'name': site.name,
        'status': site.status,
        'latitude': site.latitude,
        'longitude': site.longitude,
        'note': site.note,
    }


@router.get('/{project_id}/sites', response_model=list[SiteRead])
def list_sites_for_project(
    project_id: int,
    current_user: dict[str, str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict[str, object]]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return [
        {
            'id': site.id,
            'project_id': site.project_id,
            'name': site.name,
            'status': site.status,
            'latitude': site.latitude,
            'longitude': site.longitude,
            'note': site.note,
        }
        for site in project.sites
    ]
