import pytest

from app.api.v1.packages.schemas import RegisterPackageSchema, PackageTypeCreateSchema


@pytest.fixture
def new_package():
    return RegisterPackageSchema(
        title='Test Package',
        weight=100.19,
        price=200.5,
        type_id=1,
        owner_id=1,
    )


@pytest.fixture
def new_pac_type():
    return PackageTypeCreateSchema(
        name='TestType'
    )
