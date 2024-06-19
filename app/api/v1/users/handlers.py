from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from punq import Container

from app.api.v1.users.schemas import UserCreateSchema, UserSchema
from app.di import get_container
from app.domain.exceptions.base import ApplicationException
from app.logic.services.users.base import BaseUserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    '/',
    response_model=UserSchema,
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )
