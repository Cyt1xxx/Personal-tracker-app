def test_create_user(client):
    user_data = {
        "username": "BobTheGoa8095",
        "password": "12345678",
        "email": None
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert "password" not in response.json()
    assert "username" in response.json()
    assert "id" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()

