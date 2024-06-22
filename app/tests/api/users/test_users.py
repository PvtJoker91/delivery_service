import pytest
from fastapi import FastAPI
from httpx import Response
from starlette.testclient import TestClient

from app.api.v1.users.schemas import UserCreateSchema


@pytest.mark.asyncio
async def test_basic_auth(
        app: FastAPI,
        client: TestClient,
        auth_user: tuple,
):
    url = app.url_path_for('basic_auth')
    response: Response = client.post(url=url, auth=auth_user)

    assert response.is_success


@pytest.mark.asyncio
async def test_basic_auth_wrong_creds_exception(
        app: FastAPI,
        client: TestClient,
):
    url = app.url_path_for('basic_auth')
    response: Response = client.post(url=url, auth=('wrong_username', 'wrong_password'))

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_add_user(
        app: FastAPI,
        client: TestClient,
        new_user: UserCreateSchema
):
    url = app.url_path_for('add_user')
    response: Response = client.post(url=url, json=new_user.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_add_user_same_username_exception(
        app: FastAPI,
        client: TestClient,
        new_user: UserCreateSchema,
        auth_user: tuple,
):
    new_user.username = auth_user[0]
    url = app.url_path_for('add_user')
    response: Response = client.post(url=url, json=new_user.model_dump())

    assert response.status_code == 400
