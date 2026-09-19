from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_site_geometry_is_saved_and_retrieved() -> None:
    register_payload = {
        'email': 'geo@example.com',
        'password': 'Password123!',
        'full_name': 'Geo User',
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
            'name': 'Ewaso Basin Restoration',
            'country': 'Kenya',
            'status': 'active',
            'budget': 120000,
            'description': 'Watershed restoration and monitoring.',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert project_response.status_code == 201, project_response.text
    project_id = project_response.json()['id']

    site_response = client.post(
        f'/projects/{project_id}/sites',
        json={
            'name': 'Ridge Segment A',
            'status': 'monitoring',
            'latitude': -1.2,
            'longitude': 36.8,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert site_response.status_code == 201, site_response.text
    site_id = site_response.json()['id']

    geometry = {
        'type': 'Polygon',
        'coordinates': [
            [[36.8, -1.2], [36.9, -1.2], [36.9, -1.1], [36.8, -1.1], [36.8, -1.2]],
        ],
    }

    geometry_response = client.post(
        f'/sites/{site_id}/geometry',
        json=geometry,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert geometry_response.status_code == 201, geometry_response.text
    payload = geometry_response.json()
    assert payload['type'] == 'Polygon'
    assert payload['coordinates'][0][0] == [36.8, -1.2]

    lookup_response = client.get(f'/sites/{site_id}', headers={'Authorization': f'Bearer {token}'})
    assert lookup_response.status_code == 200, lookup_response.text
    assert lookup_response.json()['geometry']['type'] == 'Polygon'
