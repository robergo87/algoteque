import pytest

from app import application

@pytest.fixture
def app():
    yield application

@pytest.fixture
def client(app):
    return app.test_client()

def test_sample_generic(client):
    json_req = {
        "topics": {
            "reading": 20,
            "math": 50,
            "science": 30,
            "history": 15,
            "art": 10
        }
    }
    expected_dict = {
        "provider_a": 8,
        "rovider_b": 5,
        "provider_c": 12.5
    }
    
    response = client.post('/api/recommend/', json=json_req)
    assert response.status_code == 200
    resp_json = response.get_json()
    
    assert isinstance(resp_json, list)
    mapping = {row["provider"]: row["quote"] for row in resp_json}    
    for provider, quote in expected_dict:
        assert mapping.get(provider) == quote