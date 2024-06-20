from logging import Logger

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from punq import Container

from app.api.v1.users.dependencies import get_auth_user
from app.api.v1.users.schemas import UserCreateSchema, UserSchema
from app.di import get_container
from app.domain.exceptions.base import ApplicationException
from app.logic.services.users.base import BaseUserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    '/auth',
    response_model=UserSchema,
    description='Эндпоинт для BasicAuth',
    status_code=status.HTTP_200_OK,
)
async def basic_auth(
        user: UserSchema = Depends(get_auth_user),
        container: Container = Depends(get_container),
):
    try:
        return user
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )


@router.post(
    '/',
    response_model=UserSchema,
    description='Эндпоинт добавляет нового пользователя. Ошибка 400 при неуникальном username',
    status_code=status.HTTP_201_CREATED
)
async def add_user(
        user: UserCreateSchema,
        container: Container = Depends(get_container),
):
    service: BaseUserService = container.resolve(BaseUserService)
    try:
        user = await service.create_user(user_in=user.to_entity())
        return UserSchema.from_entity(user)
    except ApplicationException as exception:
        logger: Logger = container.resolve(Logger)
        logger.error(msg=exception.message)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
