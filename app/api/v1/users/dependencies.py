from typing import Annotated

from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from punq import Container

from app.api.exceptions import WrongCredentialsAPIException
from app.api.v1.users.schemas import UserSchema
from app.di import get_container
from app.domain.exceptions.base import ApplicationException
from app.logic.services.users.base import BaseUserService
from app.logic.utils import validate_password

security = HTTPBasic()


async def get_auth_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        container: Container = Depends(get_container)
):
    service: BaseUserService = container.resolve(BaseUserService)
    try:
        user = await service.get_user_by_username(username=credentials.username)
        validate_password(password=credentials.password, hashed_password=user.password.as_generic_type())
    except ApplicationException:
        raise WrongCredentialsAPIException
    return UserSchema.from_entity(user)
