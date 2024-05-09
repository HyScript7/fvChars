import pytest
from fastapi import status
from httpx import AsyncClient

from .. import client
from . import V1_ROUTE

USERS_ROOT: str = V1_ROUTE + "/users"
REGISTER_ROUTE: str = USERS_ROOT + "/register"
LOGIN_ROUTE: str = USERS_ROOT + "/login"
DELETE_ROUTE: str = USERS_ROOT + "/delete"
UPDATE_DISPLAYNAME_ROUTE: str = USERS_ROOT + "/update/displayname"
UPDATE_PASSWORD_ROUTE: str = USERS_ROOT + "/update/password"
WHOAMI_ROUTE: str = USERS_ROOT + "/whoami"


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_register_bad_entity(client: AsyncClient):
    res = await client.post(
        "/api/v1/users/register",
        json={},
    )
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_register_nodisplay(client: AsyncClient):
    res = await client.post(
        "/api/v1/users/register",
        json={
            "username": "johndoe",
            "password": "foobar",
            "email": "johndoe@example.com",
        },
    )
    assert res.status_code == status.HTTP_201_CREATED
    res_body = res.json()
    assert res_body.get("displayname") == "johndoe"
    assert res_body.get("username") == "johndoe"


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_register_with_display(client: AsyncClient):
    res = await client.post(
        REGISTER_ROUTE,
        json={
            "displayname": "Jane Doe",
            "username": "janedoe",
            "password": "foobar",
            "email": "janedoe@example.com",
        },
    )
    assert res.status_code == status.HTTP_201_CREATED
    res_body = res.json()
    assert res_body.get("displayname") == "Jane Doe"
    assert res_body.get("username") == "janedoe"


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_register_taken_username(client: AsyncClient):
    res = await client.post(
        REGISTER_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
            "email": "notjohndoe@example.com",
        },
    )
    assert res.status_code == status.HTTP_409_CONFLICT


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_register_taken_email(client: AsyncClient):
    res = await client.post(
        REGISTER_ROUTE,
        json={
            "username": "notjohndoe",
            "password": "foobar",
            "email": "johndoe@example.com",
        },
    )
    assert res.status_code == status.HTTP_409_CONFLICT


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_bad_entity(client: AsyncClient):
    res = await client.post(
        LOGIN_ROUTE,
        json={},
    )
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_bad_password(client: AsyncClient):
    res = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "notfoobar",
        },
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    res = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
        },
    )
    assert res.status_code == status.HTTP_200_OK
    res_body = res.json()
    assert res_body.get("token") is not None


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_root_guest(client: AsyncClient):
    res = await client.get(
        USERS_ROOT + "/",
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello Guest"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_root_bad_token(client: AsyncClient):
    res = await client.get(
        USERS_ROOT + "/",
        headers={"jwt-token": "not.valid.token"},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello Guest"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_root_valid_token(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "janedoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.get(
        USERS_ROOT + "/",
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("message") == "Hello Jane Doe"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_whoami_bad_token(client: AsyncClient):
    res = await client.get(
        WHOAMI_ROUTE,
        headers={"jwt-token": "not.valid.token"},
    )
    assert res.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
    assert res.json().get("username") == "guest"
    assert res.json().get("displayname") == "Guest"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_whoami(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "janedoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.get(
        WHOAMI_ROUTE,
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("username") == "janedoe"
    assert res.json().get("displayname") == "Jane Doe"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_displayname_bad_token(client: AsyncClient):
    res = await client.put(
        UPDATE_DISPLAYNAME_ROUTE,
        json={"displayname": "John Doe"},
        headers={"jwt-token": "not.valid.token"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_displayname(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.put(
        UPDATE_DISPLAYNAME_ROUTE,
        json={"displayname": "John Doe"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get("displayname") == "John Doe"


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_delete_bad_password(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.request(
        "DELETE",
        DELETE_ROUTE,
        json={"current_password": "bazbar"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_delete_bad_token(client: AsyncClient):
    res = await client.request(
        "DELETE",
        DELETE_ROUTE,
        json={"current_password": "foobar"},
        headers={"jwt-token": "not.valid.token"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_delete_bad_entity(client: AsyncClient):
    res = await client.request("DELETE", DELETE_ROUTE, json={}, headers={})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_changepassword_bad_entity(client: AsyncClient):
    res = await client.post(UPDATE_PASSWORD_ROUTE, json={}, headers={})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_changepassword_bad_current_password(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.post(
        UPDATE_PASSWORD_ROUTE,
        json={"current_password": "notfoobar", "new_password": "foobarbaz"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_changepassword_bad_token(client: AsyncClient):
    res = await client.post(
        UPDATE_PASSWORD_ROUTE,
        json={"current_password": "foobar", "new_password": "foobarbaz"},
        headers={"jwt-token": "not.valid.token"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_changepassword(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.post(
        UPDATE_PASSWORD_ROUTE,
        json={"current_password": "foobar", "new_password": "foobarbaz"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_delete(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "johndoe",
            "password": "foobarbaz",
        },
    )
    token = login_response.json().get("token")
    res = await client.request(
        "DELETE",
        DELETE_ROUTE,
        json={"current_password": "foobarbaz"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_delete_jane(client: AsyncClient):
    login_response = await client.post(
        LOGIN_ROUTE,
        json={
            "username": "janedoe",
            "password": "foobar",
        },
    )
    token = login_response.json().get("token")
    res = await client.request(
        "DELETE",
        DELETE_ROUTE,
        json={"current_password": "foobar"},
        headers={"jwt-token": token},
    )
    assert res.status_code == status.HTTP_200_OK
