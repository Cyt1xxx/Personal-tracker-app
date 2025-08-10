from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_create_user():
    user_data = {
        "username": "BobTheGoa809",
        "password": "12345678",
        "email": None
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
