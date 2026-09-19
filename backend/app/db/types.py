from sqlalchemy import String
from sqlalchemy.types import TypeDecorator
from geoalchemy2 import Geometry


class SpatialGeometry(TypeDecorator):
    """Use native PostGIS geometry in production and JSON text in SQLite."""

    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(
                Geometry(geometry_type='GEOMETRY', srid=4326, spatial_index=True)
            )
        return dialect.type_descriptor(String())
