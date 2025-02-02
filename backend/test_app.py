import pytest

from app import application

@pytest.fixture
def app():
    yield application

@pytest.fixture
def client(app):
    return app.test_client()


def recommendation_test(client, json_req, expected_dict):
    response = client.post('/api/recommend/', json=json_req)
    assert response.status_code == 200
    resp_json = response.get_json()
    
    assert isinstance(resp_json, list)
    mapping = {row["provider"]: row["quote"] for row in resp_json}    
    for provider, quote in expected_dict.items():
        assert abs(mapping.get(provider) - quote) < 0.0001
        
        
def test_from_given_example(client):
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
        "provider_a": 8.0,
        "provider_b": 5.0,
        "provider_c": 12.5
    }
    recommendation_test(client, json_req, expected_dict)


def test_from_given_example_fixed(client):
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
        "provider_a": 8.0,
        "provider_b": 5.0,
        "provider_c": 10.0
    }
    recommendation_test(client, json_req, expected_dict)


def test_alternative_example(client):
    json_req = {
        "topics": {
            "reading": 20,
            "math": 50,
            "science": 30,
            "history": 40,
            "art": 10
        }
    }
    expected_dict = {
        "provider_a": 8.0,
        "provider_b": 9.0,
        "provider_c": 9.0
    }
    recommendation_test(client, json_req, expected_dict)
