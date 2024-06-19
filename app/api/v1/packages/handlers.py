from typing import Iterable

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from punq import Container

from app.api.filters import PaginationIn, PaginationOut
from app.api.schemas import ListPaginatedResponse
from app.api.v1.packages.filters import PackageFilter
from app.api.v1.packages.schemas import RegisterPackageSchema, RegisterPackageResponseSchema, PackageSchema, \
    PackageDetailSchema, PackageTypeSchema, PackageTypeCreateSchema
from app.di import get_container
from app.domain.exceptions.base import ApplicationException
from app.logic.services.packages.base import BasePackageService

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.post(
    '/register',
    response_model=RegisterPackageResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_package(
        package_in: RegisterPackageSchema,
        container: Container = Depends(get_container),
) -> RegisterPackageResponseSchema:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        package = await service.register_package(package=package_in.to_entity())
        return RegisterPackageResponseSchema.from_entity(package)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/my_packages',
    status_code=status.HTTP_201_CREATED
)
async def my_packages(
        pagination_in: PaginationIn = Depends(),
        filters: PackageFilter = Depends(),
        container: Container = Depends(get_container),
) -> ListPaginatedResponse[PackageSchema]:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        packages = await service.get_package_list(pagination=pagination_in, filters=filters.to_entity())
        count = await service.get_package_count(filters=filters.to_entity())
        items = [PackageSchema.from_entity(package) for package in packages]
        pagination = PaginationOut(
            offset=pagination_in.offset,
            limit=pagination_in.limit,
            total=count,
        )
        return ListPaginatedResponse[PackageSchema](items=items, pagination=pagination)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/type_list',
    response_model=Iterable[PackageTypeSchema],
    status_code=status.HTTP_200_OK
)
async def package_types(
        container: Container = Depends(get_container),
) -> list[PackageTypeSchema]:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        p_types = await service.get_package_types_list()
        return [PackageTypeSchema.from_entity(p_type) for p_type in p_types]
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/{package_id}',
    response_model=PackageDetailSchema,
    status_code=status.HTTP_200_OK
)
async def package_detail(
        package_id: int,
        container: Container = Depends(get_container),
) -> PackageDetailSchema:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        package = await service.get_package(package_id=package_id)
        return PackageDetailSchema.from_entity(package)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.post(
    '/add_type',
    response_model=PackageTypeSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_package_type(
        p_type: PackageTypeCreateSchema,
        container: Container = Depends(get_container),
) -> PackageTypeSchema:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        p_type = await service.add_package_type(p_type.to_entity())
        return PackageTypeSchema.from_entity(p_type)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
