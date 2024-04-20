import pytest

from . import client


@pytest.mark.order(1)
def test_chars_create_one():
    register_response = client.post(
        "/api/v1/user/register",
        json={
            "username": "janedoe",
            "password": "foobar",
            "email": "example2@example.com",
        },
    )
    userid = register_response.json().get("id", 1)
    token_response = client.post(
        "/api/v1/user/login", json={"username": "janedoe", "password": "foobar"}
    )
    token = token_response.json().get("token")
    response = client.post("/api/v1/character/create", params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "userid": userid}


@pytest.mark.order(2)
def test_chars_create_two():
    token_response = client.post(
        "/api/v1/user/login", json={"username": "janedoe", "password": "foobar"}
    )
    userid = token_response.json().get("id", 1)
    token = token_response.json().get("token")
    response = client.post("/api/v1/character/create", params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"id": 2, "userid": userid}


@pytest.mark.order(3)
def test_chars_fetch_all():
    token_response = client.post(
        "/api/v1/user/login", json={"username": "janedoe", "password": "foobar"}
    )
    userid = token_response.json().get("id", 1)
    token = token_response.json().get("token")
    response = client.get("/api/v1/character/get", params={"token": token})
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "userid": userid},
        {"id": 2, "userid": userid},
    ]


def test_chars_create_unauthorized():
    response = client.post("/api/v1/character/create")
    assert response.status_code == 401


def test_chars_create_unauthorized_invalidtoken():
    response = client.post("/api/v1/character/create", params={"token": "foo.bar.baz"})
    assert response.status_code == 401


def test_chars_fetch_all_unauthorized():
    response = client.get("/api/v1/character/get")
    assert response.status_code == 401


def test_chars_fetch_all_unauthorized_invalidtoken():
    response = client.get("/api/v1/character/get", params={"token": "foo.bar.baz"})
    assert response.status_code == 401
