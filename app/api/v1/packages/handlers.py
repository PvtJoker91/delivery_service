from logging import Logger
from typing import Iterable

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from punq import Container
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.filters import PaginationIn, PaginationOut
from app.api.schemas import ListPaginatedResponse
from app.api.v1.packages.filters import PackageFilter
from app.api.v1.packages.schemas import RegisterPackageSchema, RegisterPackageResponseSchema, PackageSchema, \
    PackageDetailSchema, PackageTypeSchema, PackageTypeCreateSchema
from app.api.v1.users.dependencies import get_auth_user
from app.api.v1.users.schemas import UserSchema
from app.di import get_container
from app.domain.entities.packages import PackageFilter as PackageFilterEntity
from app.domain.exceptions.base import ApplicationException
from app.infra.db.session import init_async_session
from app.infra.repositories.packages.alchemy import SQLAlchemyPackageRepository
from app.infra.workers.celery.celery_tasks import calculate_delivery_cost_task
from app.logic.services.packages.base import BasePackageService

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.post(
    '/register',
    response_model=RegisterPackageResponseSchema,
    description='Эндпоинт регистрирует новую посылку без рассчета стоимости доставки',
    status_code=status.HTTP_201_CREATED
)
async def register_package(
        package_in: RegisterPackageSchema,
        user: UserSchema = Depends(get_auth_user),
        container: Container = Depends(get_container),
) -> RegisterPackageResponseSchema:
    package_in.owner_id = user.id
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        package = await service.register_package(package=package_in.to_entity())
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return RegisterPackageResponseSchema.from_entity(package)


@router.get(
    '/my_packages',
    description='Эндпоинт выдает список посылок текущего пользователя с фильтрацией и пагинацией',
    status_code=status.HTTP_201_CREATED
)
async def my_packages(
        user: UserSchema = Depends(get_auth_user),
        pagination_in: PaginationIn = Depends(),
        filters: PackageFilter = Depends(),
        container: Container = Depends(get_container),
) -> ListPaginatedResponse[PackageSchema]:
    comb_filter = PackageFilterEntity(type_id=filters.type_id, user_id=user.id, is_calculated=filters.is_calculated)
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        packages = await service.get_package_list(pagination=pagination_in, filters=comb_filter)
        count = await service.get_package_count(filters=comb_filter)
        items = [PackageSchema.from_entity(package) for package in packages]
        pagination = PaginationOut(
            offset=pagination_in.offset,
            limit=pagination_in.limit,
            total=count,
        )
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return ListPaginatedResponse[PackageSchema](items=items, pagination=pagination)


@router.get(
    '/type_list',
    response_model=Iterable[PackageTypeSchema],
    description='Эндпоинт выдает список всех типов посылок',
    status_code=status.HTTP_200_OK
)
async def package_types(
        container: Container = Depends(get_container),
) -> list[PackageTypeSchema]:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        p_types = await service.get_package_types_list()
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return [PackageTypeSchema.from_entity(p_type) for p_type in p_types]




@router.get('/test_session')
async def test_session(
        session: AsyncSession = Depends(init_async_session)
):
    raise Exception(session)
    repository = SQLAlchemyPackageRepository(session)
    types_list = await repository.get_package_types_list()
    return types_list



@router.get(
    '/{package_id}',
    response_model=PackageDetailSchema,
    description='Эндпоинт выдает детальные данные о посылке по ее ID',
    status_code=status.HTTP_200_OK
)
async def package_detail(
        package_id: int,
        container: Container = Depends(get_container),
) -> PackageDetailSchema:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        package = await service.get_package(package_id=package_id)
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return PackageDetailSchema.from_entity(package)


@router.post(
    '/add_type',
    response_model=PackageTypeSchema,
    description='Эндпоинт добавляет новый тип посылки, или возвращает ошибку 400, если такой тип существует',
    status_code=status.HTTP_201_CREATED
)
async def add_package_type(
        p_type: PackageTypeCreateSchema,
        container: Container = Depends(get_container),
) -> PackageTypeSchema:
    service: BasePackageService = container.resolve(BasePackageService)
    try:
        p_type = await service.add_package_type(p_type.to_entity())
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return PackageTypeSchema.from_entity(p_type)


@router.post(
    '/calculate',
    description='Эндпоинт принудительно запускает задачу рассчёта стоимости доставки для всех нерассчитанных посылок',
    status_code=status.HTTP_200_OK
)
async def calculate_cost() -> JSONResponse:
    try:
        task = calculate_delivery_cost_task.delay()
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
    return JSONResponse(content={'ID задачи': task.id, 'Статус задачи': AsyncResult(task.id).status})
