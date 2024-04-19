from . import client
from base64 import b64decode


def test_register_badbody():
    response = client.post("/api/v1/user/register", json={"foo": "bar"})
    assert response.status_code == 422


def test_register_goodbody():
    response = client.post(
        "/api/v1/user/register",
        json={
            "username": "johndoe",
            "password": "foobar",
            "email": "example@example.com",
        },
    )
    assert response.status_code == 200
    assert response.json().get("id") != None
    assert response.json() == {
        "username": "johndoe",
        "id": response.json().get("id", 1),
        "email": "example@example.com",
    }


def test_register_conflict_email():
    response = client.post(
        "/api/v1/user/register",
        json={
            "username": "johndoe1",
            "password": "foobar",
            "email": "example@example.com",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already taken"}


def test_register_conflict_username():
    response = client.post(
        "/api/v1/user/register",
        json={
            "username": "johndoe",
            "password": "foobar",
            "email": "example1@example.com",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Username already taken"}


def test_login_badbody():
    response = client.post("/api/v1/user/login", json={"foo": "bar"})
    assert response.status_code == 422


def test_login_goodbody_badusername():
    response = client.post(
        "/api/v1/user/login", json={"username": "johndoe1", "password": "foobar"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_login_goodbody_badpassword():
    response = client.post(
        "/api/v1/user/login", json={"username": "johndoe", "password": "foobar1"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_good():
    response = client.post(
        "/api/v1/user/login", json={"username": "johndoe", "password": "foobar"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response.get("token") != None
    json_response.pop("token")
    assert response.json().get("id") != None
    assert json_response == {
        "username": "johndoe",
        "id": response.json().get("id", 1),
        "email": "example@example.com",
    }


def test_me_notoken():
    response = client.get("/api/v1/user/me")
    assert response.status_code == 200
    assert response.json() == {"username": "guest", "id": 0, "email": "guest"}


def test_me_badtoken():
    response = client.get("/api/v1/user/me", params={"token": "clearly.invalid.token"})
    assert response.status_code == 200
    assert response.json() == {"username": "guest", "id": 0, "email": "guest"}


def test_me_goodtoken():
    token_response = client.post(
        "/api/v1/user/login", json={"username": "johndoe", "password": "foobar"}
    )
    token = token_response.json().get("token")
    response = client.get("/api/v1/user/me", params={"token": token})
    assert response.status_code == 200
    assert response.json().get("id") != None
    assert response.json() == {
        "username": "johndoe",
        "id": response.json().get("id", 1),
        "email": "example@example.com",
    }
