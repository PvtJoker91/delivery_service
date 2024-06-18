from fastapi import APIRouter, HTTPException, status

from app.api.filters import PaginationIn
from app.api.schemas import ListPaginatedResponse, ApiResponse
from app.api.v1.packages.filters import PackageFilter
from app.api.v1.packages.schemas import RegisterPackageSchema, RegisterPackageResponseSchema, PackageSchema, \
    PackageDetailSchema, PackageTypeSchema
from app.domain.exceptions.base import ApplicationException

router = APIRouter(prefix="/packages", tags=["Tasks"])


@router.post(
    '/register',
    response_model=RegisterPackageResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_package(
        package_in: RegisterPackageSchema,
) -> RegisterPackageResponseSchema:
    use_case: RegisterPackageUseCase = container.resolve(RegisterPackageUseCase)
    try:
        package = await use_case.execute(package_in=package_in.to_entity())
        return RegisterPackageResponseSchema.from_entity(package)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/my_packages',
    response_model=RegisterPackageResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def my_packages(
        pagination_in: PaginationIn,
        filters: PackageFilter
) -> ApiResponse[ListPaginatedResponse[PackageSchema]]:
    use_case: GetMyPackagesUseCase = container.resolve(GetMyPackagesUseCase)
    try:
        packages = await use_case.execute(pagination_in=pagination_in, filters=filters)
        return ApiResponse(
            data=ListPaginatedResponse(
                items=[PackageSchema.from_entity(package) for package in packages],
                pagination=1
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/{package_oid}',
    response_model=PackageDetailSchema,
    status_code=status.HTTP_200_OK
)
async def package_detail(
        package_oid: str
) -> PackageDetailSchema:
    use_case: GetPackageDetailUseCase = container.resolve(GetPackageDetailUseCase)
    try:
        package = await use_case.execute(package_oid=package_oid)
        return PackageDetailSchema.from_entity(package)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.get(
    '/types',
    response_model=PackageTypeSchema,
    status_code=status.HTTP_200_OK
)
async def package_types() -> list[PackageTypeSchema]:
    use_case: GetPackageTypesUseCase = container.resolve(GetPackageTypesUseCase)
    try:
        p_types = await use_case.execute()
        return [PackageTypeSchema.from_entity(p_type) for p_type in p_types]
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
