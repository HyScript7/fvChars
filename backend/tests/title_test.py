import pytest

from . import client

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


@pytest.mark.order(1)
def test_titles_create_one():
    response = client.post(
        "/api/v1/title/create", params={"token": token}, json={"title": "Foobar"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "userid": userid, "title": "Foobar"}


@pytest.mark.order(2)
def test_titles_create_two():
    response = client.post(
        "/api/v1/title/create", params={"token": token}, json={"title": "Foobarbaz"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 2, "userid": userid, "title": "Foobarbaz"}


@pytest.mark.order(3)
def test_titles_get_all_own():
    response = client.get("/api/v1/title/own", params={"token": token})
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "userid": userid, "title": "Foobar"},
        {"id": 2, "userid": userid, "title": "Foobarbaz"},
    ]


@pytest.mark.order(2)
def test_titles_create_duplicate():
    response = client.post(
        "/api/v1/title/create", params={"token": token}, json={"title": "Foobar"}
    )
    assert response.status_code == 409
