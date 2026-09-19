from sqlalchemy import select

from app.db.session import SessionLocal
from app.main import app
from app.models.user import User


def test_registration_persists_users_in_database() -> None:
    with SessionLocal() as session:
        session.query(User).delete()
        session.commit()

    client = __import__('fastapi.testclient').testclient.TestClient(app)
    response = client.post(
        '/auth/register',
        json={'email': 'db-user@example.com', 'password': 'Password123!', 'full_name': 'DB User'},
    )
    assert response.status_code == 201, response.text

    with SessionLocal() as session:
        users = session.scalars(select(User)).all()
    assert len(users) == 1
    assert users[0].email == 'db-user@example.com'
