from collections.abc import Generator

import pytest
from sqlalchemy import delete

from app.db.session import SessionLocal
from app.models.project import Project, Site
from app.models.user import User


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    with SessionLocal() as session:
        session.execute(delete(Site))
        session.execute(delete(Project))
        session.execute(delete(User))
        session.commit()

    yield

    with SessionLocal() as session:
        session.execute(delete(Site))
        session.execute(delete(Project))
        session.execute(delete(User))
        session.commit()
