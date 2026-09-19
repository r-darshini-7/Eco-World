import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_roles
from app.db.session import get_db
from app.models.project import Site
from app.schemas.geospatial import GeometryPayload, SiteWithGeometry

router = APIRouter(tags=['geospatial'])


@router.post('/sites/{site_id}/geometry', response_model=GeometryPayload, status_code=status.HTTP_201_CREATED)
def save_site_geometry(
    site_id: int,
    payload: GeometryPayload,
    current_user: dict[str, str] = Depends(require_roles('ADMIN')),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    site = db.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Site not found')

    geometry_json = json.dumps(payload.model_dump())
    if db.bind and db.bind.dialect.name == 'postgresql':
        site.geometry = func.ST_SetSRID(func.ST_GeomFromGeoJSON(geometry_json), 4326)
    else:
        site.geometry = geometry_json
    db.add(site)
    db.commit()
    db.refresh(site)
    return payload.model_dump()


@router.get('/sites/{site_id}', response_model=SiteWithGeometry)
def get_site_details(
    site_id: int,
    current_user: dict[str, str] = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    site = db.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Site not found')

    geometry = None
    if db.bind and db.bind.dialect.name == 'postgresql':
        geometry_json = db.scalar(
            select(func.ST_AsGeoJSON(Site.geometry)).where(Site.id == site_id)
        )
        if geometry_json:
            geometry = json.loads(geometry_json)
    elif site.geometry:
        geometry = json.loads(site.geometry)

    return {
        'id': site.id,
        'project_id': site.project_id,
        'name': site.name,
        'status': site.status,
        'latitude': site.latitude,
        'longitude': site.longitude,
        'note': site.note,
        'geometry': geometry,
    }
