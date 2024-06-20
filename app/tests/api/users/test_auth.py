from copy import copy

from httpx import Response

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest
from punq import Container

from src.apps.users.entities.users import UserEntity
from src.apps.users.services.users import BaseUserService


@pytest.mark.asyncio
async def test_user_login(
        app: FastAPI,
        client: TestClient,
        login_active_user: UserEntity,
        get_dummy_container: Container
):
    password = copy(login_active_user.password)  # почему-то юзер-сервис снизу хэширует пароль во входном login_active_user
    service = get_dummy_container.resolve(BaseUserService)
    await service.create_user(user_in=login_active_user)
    # raise Exception(login_active_user)
    url = app.url_path_for('auth_user_issue_jwt')
    response: Response = client.post(url=url, data={"username": login_active_user.username,
                                                    "password": password})
    assert response.is_success


@pytest.mark.asyncio
async def test_wrong_password_user_login(
        app: FastAPI,
        client: TestClient,
        login_active_user: UserEntity,
        get_dummy_container: Container
):
    password = "wrong"
    service = get_dummy_container.resolve(BaseUserService)
    await service.create_user(user_in=login_active_user)
    url = app.url_path_for('auth_user_issue_jwt')
    response: Response = client.post(url=url, data={"username": login_active_user.username,
                                                    "password": password})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_inactive_user_login(
        app: FastAPI,
        client: TestClient,
        login_inactive_user: UserEntity,
        get_dummy_container: Container
):
    password = copy(login_inactive_user.password)  # почему-то юзер-сервис снизу хэширует пароль во входном login_inactive_user
    service = get_dummy_container.resolve(BaseUserService)
    await service.create_user(user_in=login_inactive_user)
    url = app.url_path_for('auth_user_issue_jwt')
    response: Response = client.post(url=url, data={"username": login_inactive_user.username,
                                                    "password": password})
    assert response.status_code == 400
