import pytest
from punq import Container

from app.tests.fixtures import init_dummy_container

from app.domain.entities.packages import PackageType, Package
from app.domain.entities.users import User
from app.domain.values.packages import Title, PackageWeight, PackagePrice
from app.domain.values.users import UserName, Password


@pytest.fixture
def get_dummy_container() -> Container:
    return init_dummy_container()


@pytest.fixture
def user_entity():
    return User(username=UserName('test_user'), password=Password('test_password'))


@pytest.fixture
def package_type_entity():
    return PackageType(name=Title('test_type'))


@pytest.fixture
def package_entity():
    return Package(
        title=Title('test_package'),
        weight=PackageWeight(100.00),
        price=PackagePrice(300.1),
        type_id=1,
        owner_id=1,
        type=PackageType(name=Title('test_type')),
        owner=User(username=UserName('test_user'), password=Password('test_password')),
    )
