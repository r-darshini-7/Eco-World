from typing import Literal

from pydantic import BaseModel, Field

ProjectStatus = Literal['draft', 'active', 'paused', 'completed']
SiteStatus = Literal['planned', 'monitoring', 'flagged', 'resolved']


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    country: str = Field(..., min_length=2, max_length=120)
    status: ProjectStatus = 'draft'
    budget: float = Field(default=0.0, ge=0)
    description: str | None = Field(default=None, max_length=2000)


class ProjectRead(ProjectCreate):
    id: int
    site_count: int = 0


class SiteCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    status: SiteStatus = 'planned'
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    note: str | None = Field(default=None, max_length=1000)


class SiteRead(SiteCreate):
    id: int
    project_id: int
