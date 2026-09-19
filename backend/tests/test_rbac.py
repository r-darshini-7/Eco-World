from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.session import SessionLocal
from app.main import app
from app.models.user import User

client = TestClient(app)


def test_viewer_can_read_but_cannot_create_projects() -> None:
    register_payload = {
        'email': 'viewer@example.com',
        'password': 'Password123!',
        'full_name': 'Read Only User',
    }
    register_response = client.post('/auth/register', json=register_payload)
    assert register_response.status_code == 201, register_response.text

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == register_payload['email']))
        assert user is not None
        user.role = 'VIEWER'
        db.commit()

    login_response = client.post(
        '/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    read_response = client.get('/projects', headers=headers)
    assert read_response.status_code == 200, read_response.text

    create_response = client.post(
        '/projects',
        json={'name': 'Blocked Project', 'country': 'Kenya', 'status': 'draft', 'budget': 0},
        headers=headers,
    )
    assert create_response.status_code == 403, create_response.text
