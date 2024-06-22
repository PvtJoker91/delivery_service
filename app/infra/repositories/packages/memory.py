import uuid
from typing import Iterable

from app.domain.entities.packages import PackageFilter
from app.infra.exceptions.packages import PackageNotFoundException, PackageTypeAlreadyExistsException
from app.infra.db.packages import PackageType, Package
from app.infra.db.users import User
from app.infra.repositories.packages.base import BasePackageRepository


class MemoryPackageRepository(BasePackageRepository):
    saved_packages: dict[int: Package] = {
        1: Package(
            id=1,
            title='TestPackage',
            weight=100.0,
            price=200.0,
            delivery_cost=None,
            type_id=1,
            owner_id=1,
            owner=User(id=1, username='user1', password='0xb123123'),
            type=PackageType(id=1, name='Type1')

        )
    }
    saved_package_types: dict[int: PackageType] = {
        1: PackageType(
            id=1,
            name='Type1'
        )
    }

    async def add_package(self, package: Package) -> Package:
        package.id = int(uuid.uuid4())
        package.type = PackageType(id=1, name='Type1')
        package.owner = User(
            id=1,
            username='user1',
            password=b'$2b$12$T0Eb3Yfp9KcwZiUchYBbr.TbxHbDhgJnrq1EV9/RrFU0dIBbUXJta'
        )
        self.saved_packages[package.id] = package
        return package

    async def update_package_list_delivery_cost(self, package_dto_list: Iterable[Package]) -> None:
        for pack in package_dto_list:
            if pack.id in self.saved_packages:
                self.saved_packages[pack.id].delivery_cost = pack.delivery_cost

    async def get_not_calculated_package_list(self) -> Iterable[Package]:
        not_calc = []
        for pack in self.saved_packages.values():
            if pack.delivery_cost is None:
                not_calc.append(pack)
        return not_calc

    async def get_package(self, package_id: int) -> Package:
        for pack in self.saved_packages.values():
            if pack.id == package_id:
                return pack
        raise PackageNotFoundException

    async def get_package_list(self, pagination, filters: PackageFilter) -> Iterable[Package]:
        return self.saved_packages.values()

    async def get_package_count(self, filters: PackageFilter) -> int:
        return len(self.saved_packages)

    async def add_package_type(self, p_type: PackageType) -> PackageType:
        p_type.id = int(uuid.uuid4())
        for t in self.saved_package_types.values():
            if t.name == p_type.name:
                raise PackageTypeAlreadyExistsException
        self.saved_package_types[p_type.id] = p_type
        return p_type

    async def get_package_types_list(self) -> Iterable[PackageType]:
        return self.saved_package_types.values()
