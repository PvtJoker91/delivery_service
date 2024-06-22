import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.di import get_container
from app.tests.fixtures import init_dummy_container
from main import create_app


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_container] = init_dummy_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def auth_user() -> tuple:
    return 'user1', 'test_password'
