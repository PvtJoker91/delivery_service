import pytest

from src.apps.users.entities.users import UserEntity


@pytest.fixture(scope="function")
def login_active_user() -> UserEntity:
    return UserEntity(
        username="test_user",
        password="test_pass",
        email="user@user.ru",
        is_active=True,
    )


@pytest.fixture(scope="function")
def login_inactive_user() -> UserEntity:
    return UserEntity(
        username="test_inactive_user",
        password="test_pass",
        email="user@user.ru",
        is_active=False,
    )
