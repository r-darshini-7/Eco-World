from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_flow() -> None:
    register_payload = {
        'email': 'admin@example.com',
        'password': 'Password123!',
        'full_name': 'System Admin',
    }

    register_response = client.post('/auth/register', json=register_payload)
    assert register_response.status_code == 201, register_response.text
    created = register_response.json()
    assert created['email'] == register_payload['email']
    assert 'password' not in created

    login_response = client.post(
        '/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert 'access_token' in token_data
    assert token_data['token_type'] == 'bearer'

    me_response = client.get(
        '/auth/me',
        headers={'Authorization': f"Bearer {token_data['access_token']}"},
    )
    assert me_response.status_code == 200, me_response.text
    assert me_response.json()['email'] == register_payload['email']
