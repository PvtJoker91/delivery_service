from dataclasses import dataclass

from app.domain.entities.users import User as UserEntity
from app.domain.exceptions.users import PasswordValidationException
from app.domain.values.users import Password

from app.logic.services.users.base import BaseUserService
from app.logic.utils import hash_password, validate_password
from app.infra.repositories.users.base import BaseUserRepository
from app.infra.repositories.users.converters import convert_user_entity_to_model


@dataclass
class ORMUserService(BaseUserService):
    repository: BaseUserRepository
    """
    Сервис для управления пользователями, использующий ORM репозиторий для работы с базой данных.
    Attributes:
        repository (BaseUserRepository): Репозиторий для работы с пользователями.
    """

    async def create_user(self, user_in: UserEntity) -> UserEntity:
        """
        Создает нового пользователя с захешированным паролем.
        Args:
            user_in (UserEntity): Объект пользователя для создания.
        Returns:
            UserEntity: Созданный пользователь.
        """
        password = user_in.password.as_generic_type()
        hashed = hash_password(password)
        user_in.password = Password(hashed)
        user_dto = convert_user_entity_to_model(user_in)
        res_user = await self.repository.create_user(user=user_dto)
        return res_user.to_entity()

    async def get_user_by_username(self, username: str) -> UserEntity:
        """
        Получает пользователя по его имени пользователя.
        Args:
            username (str): Имя пользователя для поиска.
        Returns:
            UserEntity: Найденный пользователь.
        Raises:
            UserNotFoundException: Если пользователь не найден.
        """
        user_dto = await self.repository.get_user_by_username(username=username)
        return user_dto.to_entity()

    async def authorise_user(self, username: str, password: str) -> UserEntity:
        """
        Авторизует пользователя по его имени пользователя и паролю.
        Args:
            username (str): Имя пользователя.
            password (str): Пароль пользователя.
        Returns:
            UserEntity: Авторизованный пользователь.
        Raises:
            PasswordValidationException: Если пароль не прошел проверку.
        """
        user = await self.get_user_by_username(username=username)
        if not validate_password(password=password, hashed_password=user.password.as_generic_type()):
            raise PasswordValidationException
        return user
