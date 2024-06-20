from httpx import Response

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from src.apps.tasks.entities import TaskEntity


@pytest.mark.asyncio
async def test_create_task(
        app: FastAPI,
        client: TestClient,
        new_task: TaskEntity
):
    url = app.url_path_for('create_task')
    response: Response = client.post(url=url, json=new_task.to_dict())

    assert response.is_success


@pytest.mark.asyncio
async def test_create_task_no_assignees(
        app: FastAPI,
        client: TestClient,
        new_task: TaskEntity
):
    new_task.assignee_ids = []
    url = app.url_path_for('create_task')
    response: Response = client.post(url=url, json=new_task.to_dict())

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_task_list(
        app: FastAPI,
        client: TestClient,
):
    url = app.url_path_for('get_task_list')
    response: Response = client.get(url=url)

    assert response.is_success
