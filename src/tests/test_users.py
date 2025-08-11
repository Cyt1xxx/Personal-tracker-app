def test_get_api_endpoiny(client):
    response = client.get("/")
    assert response.status_code == 200

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

def test_create_user_with_invalid_password(client):
    response = client.post(
        "/users/",
        json={
            "username": "BobTheGoa8095",
            "email": "user2121123@example.com",
            "password": "1"
        }
    )
    assert response.status_code == 422

def test_get_user(client):
    user_data = {
        "username": "BobTheGoa8095",
        "password": "12345678",
        "email": None
    }
    response = client.post("/users/", json=user_data)
    response = client.get(f"/users/{user_data["username"]}")
    assert response.status_code == 200

def test_login_for_access_token(client):
    user_data = {
        "username": "BobTheGoa8095",
        "password": "12345678",
        "email": None
    }
    client.post("/users/", json=user_data)
    response = client.post(
        "/users/token",
        data={
            "username": "BobTheGoa8095",
            "password": "12345678",
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


