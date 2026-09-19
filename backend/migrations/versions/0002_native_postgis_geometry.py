"""Use a native PostGIS geometry column when PostgreSQL is available.

Revision ID: 0002_native_postgis_geometry
Revises: 0001_initial_schema
Create Date: 2026-09-19
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text

revision: str = '0002_native_postgis_geometry'
down_revision: Union[str, Sequence[str], None] = '0001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if op.get_bind().dialect.name == 'postgresql':
        op.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        op.execute(text(
            "ALTER TABLE sites ALTER COLUMN geometry TYPE geometry(Geometry,4326) "
            "USING CASE WHEN geometry IS NULL OR geometry = '' THEN NULL "
            "ELSE ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) END"
        ))
        op.create_index(
            'ix_sites_geometry',
            'sites',
            ['geometry'],
            postgresql_using='gist',
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == 'postgresql':
        op.drop_index('ix_sites_geometry', table_name='sites')
        op.execute(text(
            "ALTER TABLE sites ALTER COLUMN geometry TYPE text "
            "USING CASE WHEN geometry IS NULL THEN NULL ELSE ST_AsGeoJSON(geometry) END"
        ))