from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analytics_overview_returns_project_and_site_totals() -> None:
    register_payload = {
        'email': 'analytics@example.com',
        'password': 'Password123!',
        'full_name': 'Analytics User',
    }

    register_response = client.post('/auth/register', json=register_payload)
    assert register_response.status_code == 201, register_response.text

    login_response = client.post(
        '/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()['access_token']

    project_response = client.post(
        '/projects',
        json={
            'name': 'Carbon Recovery Program',
            'country': 'Uganda',
            'status': 'active',
            'budget': 225000,
            'description': 'Reforestation and biodiversity monitoring project.',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert project_response.status_code == 201, project_response.text
    project_id = project_response.json()['id']

    client.post(
        f'/projects/{project_id}/sites',
        json={
            'name': 'Lake Ado',
            'status': 'monitoring',
            'latitude': 1.234,
            'longitude': 31.987,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    client.post(
        f'/projects/{project_id}/sites',
        json={
            'name': 'Mabira Corridor',
            'status': 'flagged',
            'latitude': 0.9,
            'longitude': 32.1,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    response = client.get('/analytics/overview', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload['total_projects'] == 1
    assert payload['active_projects'] == 1
    assert payload['sites_monitored'] == 2
    assert payload['total_budget'] == 225000.0
    assert payload['project_status_breakdown']['active'] == 1
