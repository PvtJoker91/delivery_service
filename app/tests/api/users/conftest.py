import pytest
from app.api.v1.users.schemas import UserCreateSchema


@pytest.fixture
def new_user():
    return UserCreateSchema(
        username='user2',
        password='test_password'
    )
