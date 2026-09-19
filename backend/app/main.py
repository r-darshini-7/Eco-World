from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.geospatial import router as geospatial_router
from app.api.health import router as health_router
from app.api.projects import router as projects_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import project  # noqa: F401
from app.models import user  # noqa: F401

Base.metadata.create_all(bind=engine)

if settings.database_url.startswith('sqlite'):
    inspector = inspect(engine)
    if 'sites' in inspector.get_table_names():
        site_columns = {column['name'] for column in inspector.get_columns('sites')}
        if 'geometry' not in site_columns:
            with engine.begin() as connection:
                connection.execute(text('ALTER TABLE sites ADD COLUMN geometry TEXT'))

app = FastAPI(title='Darukaa.Earth API', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(analytics_router)
app.include_router(geospatial_router)


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'Darukaa.Earth backend is running'}
