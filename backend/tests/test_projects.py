from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_projects_can_be_created_and_listed() -> None:
    register_payload = {
        'email': 'project-admin@example.com',
        'password': 'Password123!',
        'full_name': 'Project Admin',
    }

    register_response = client.post('/auth/register', json=register_payload)
    assert register_response.status_code == 201, register_response.text

    login_response = client.post(
        '/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()['access_token']

    create_response = client.post(
        '/projects',
        json={
            'name': 'Restore North Valley',
            'country': 'Kenya',
            'status': 'active',
            'budget': 150000.0,
            'description': 'Forest restoration and biodiversity resilience work.',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert create_response.status_code == 201, create_response.text
    project = create_response.json()
    assert project['name'] == 'Restore North Valley'
    assert project['country'] == 'Kenya'
    assert project['status'] == 'active'
    assert project['budget'] == 150000.0

    list_response = client.get('/projects', headers={'Authorization': f'Bearer {token}'})
    assert list_response.status_code == 200, list_response.text
    payload = list_response.json()
    assert len(payload) >= 1
    assert any(item['name'] == 'Restore North Valley' for item in payload)

    site_response = client.post(
        f"/projects/{project['id']}/sites",
        json={
            'name': 'Kibwezi Ridge',
            'status': 'monitoring',
            'latitude': -1.265,
            'longitude': 37.443,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert site_response.status_code == 201, site_response.text
    site = site_response.json()
    assert site['name'] == 'Kibwezi Ridge'
    assert site['status'] == 'monitoring'
