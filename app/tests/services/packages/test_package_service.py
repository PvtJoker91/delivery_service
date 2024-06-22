import pytest

from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.infra.exceptions.packages import PackageTypeAlreadyExistsException
from app.infra.repositories.packages.memory import MemoryPackageRepository

from app.logic.services.packages.orm import ORMPackageService

service = ORMPackageService(MemoryPackageRepository())


@pytest.mark.asyncio
async def test_register_package(package_entity: PackageEntity):
    package = await service.register_package(package_entity)
    assert package_entity.title == package.title


@pytest.mark.asyncio
async def test_get_package_by_id(package_entity: PackageEntity):
    new_package = await service.register_package(package_entity)
    package_out = await service.get_package(new_package.id)
    assert new_package.title == package_out.title
    assert new_package.id == package_out.id


@pytest.mark.asyncio()
async def test_get_package_count(package_entity: PackageEntity):
    for _ in range(10):
        await service.register_package(package_entity)
    count = await service.get_package_count({})
    assert count == 14


@pytest.mark.asyncio
async def test_add_package_type(package_type_entity: PackageTypeEntity):
    p_type = await service.add_package_type(package_type_entity)
    assert p_type.name == package_type_entity.name


@pytest.mark.asyncio
async def test_add_package_type_same_name_exception(package_type_entity: PackageTypeEntity):
    with pytest.raises(PackageTypeAlreadyExistsException):
        await service.add_package_type(package_type_entity)
