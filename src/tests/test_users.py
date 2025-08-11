def test_get_api_endpoiny(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_user(client, test_user_data):
    user_data = test_user_data
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert "password" not in response.json()
    assert "username" in response.json()
    assert "id" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()

def test_create_existing_user(client, test_user_data):
    user_data = test_user_data
    client.post("/users/", json=user_data)

    response = client.post("/users/", json=user_data)
    assert response.status_code == 400

def test_create_user_with_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "username": "BobTheGoa8095",
            "email": "user2121 123 !!!", #Checkup validation for pydantic model EmailStr
            "password": "12345678" 
        }
    )

    assert response.status_code == 422

def test_create_user_with_invalid_password(client):
    response = client.post(
        "/users/",
        json={
            "username": "BobTheGoa8095",
            "email": "user2121123@example.com",
            "password": "1" #Checkup for pydantic model min_length = 8
        }
    )
    assert response.status_code == 422

def test_get_user(client, test_user_data):
    #making new user for test
    user_data = test_user_data
    response = client.post("/users/", json=user_data)

    #getting info of created user
    response = client.get(f"/users/{user_data["username"]}")
    assert response.status_code == 200

def test_login_for_access_token(client, test_user_data):
    user_data = test_user_data
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


def test_login_with_invalid_password(client, test_user_data):
    user_data = test_user_data
    client.post("/users/", json=user_data)
    response = client.post(
        "/users/token",
        data={
            "username": "BobTheGoa8095",
            "password": "fake pass",
        }
    )
    assert response.status_code == 400
    
def test_read_current_user(client, test_user_data):
    user_data = test_user_data
    client.post("/users/", json=user_data)

    token_r = client.post(
        "/users/token",
        data={
            "username": "BobTheGoa8095",
            "password": "12345678",
        }
    )
    token = token_r.json().get("access_token")
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "password" not in response.json()
    assert "username" in response.json()
    assert "id" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()

def test_read_current_user_without_auth(client):
    response = client.get("/users/me/")
    assert response.status_code == 401

