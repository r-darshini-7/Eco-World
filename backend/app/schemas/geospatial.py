from typing import Any

from pydantic import BaseModel, Field


class GeometryPayload(BaseModel):
    type: str = Field(..., min_length=2)
    coordinates: list[Any]


class SiteWithGeometry(BaseModel):
    id: int
    project_id: int
    name: str
    status: str
    latitude: float | None = None
    longitude: float | None = None
    note: str | None = None
    geometry: GeometryPayload | None = None
