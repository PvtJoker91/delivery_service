import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.packages.schemas import RegisterPackageSchema, PackageTypeCreateSchema


@pytest.mark.asyncio
async def test_register_package(
        app: FastAPI,
        client: TestClient,
        new_package: RegisterPackageSchema,
        auth_user: tuple
):
    url = app.url_path_for('add_new_package')
    response: Response = client.post(url=url, json=new_package.model_dump(), auth=auth_user)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_my_packages(
        app: FastAPI,
        client: TestClient,
        auth_user: tuple
):
    url = app.url_path_for('get_my_packages')
    params = {'offset': 0, 'limit': 20, 'type_id': 1, 'is_calculated': True}
    response: Response = client.get(url=url, auth=auth_user, params=params)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_package_types(
        app: FastAPI,
        client: TestClient,
):
    url = app.url_path_for('get_package_type_list')
    response: Response = client.get(url=url)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_package_detail(
        app: FastAPI,
        client: TestClient,
):
    pack_id = 1
    url = app.url_path_for('get_package_detail', package_id=pack_id)
    response: Response = client.get(url=url)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_package_detail_wrong_id_exception(
        app: FastAPI,
        client: TestClient,
):
    wrong_pack_id = 3
    url = app.url_path_for('get_package_detail', package_id=wrong_pack_id)
    response: Response = client.get(url=url)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_add_package_type(
        app: FastAPI,
        client: TestClient,
        new_pac_type: PackageTypeCreateSchema
):
    url = app.url_path_for('add_package_type')
    response: Response = client.post(url=url, json=new_pac_type.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_add_package_wrong_type_exception(
        app: FastAPI,
        client: TestClient,
        new_pac_type: PackageTypeCreateSchema
):
    new_pac_type.name = 'Type1'
    url = app.url_path_for('add_package_type')
    response: Response = client.post(url=url, json=new_pac_type.model_dump())

    assert response.status_code == 400
