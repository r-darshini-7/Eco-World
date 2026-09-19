from typing import Any

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import SpatialGeometry


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='draft', nullable=False)
    budget: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)

    sites: Mapped[list['Site']] = relationship(back_populates='project', cascade='all, delete-orphan')


class Site(Base):
    __tablename__ = 'sites'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default='planned', nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    note: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    geometry: Mapped[Any | None] = mapped_column(SpatialGeometry(), nullable=True)

    project: Mapped['Project'] = relationship(back_populates='sites')
