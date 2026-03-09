from fastapi.testclient import TestClient
from src.core.Models.ClientConfig import ClientConfigModel
from src.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/foxhole-updates")
    assert response.status_code == 200


def test_client_config():
    endpoint = "/foxhole-updates/config/client_config.json"
    response = client.get(endpoint)
    assert response.status_code == 200
    assert ClientConfigModel(**response.json())
