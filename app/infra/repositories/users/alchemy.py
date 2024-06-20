from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.users import UserNotFoundException, UserAlreadyExistsException
from app.infra.db.users import User
from app.infra.repositories.users.base import BaseUserRepository


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession
    """
    Репозиторий для управления пользователями, использующий SQLAlchemy для работы с базой данных.
    Attributes:
        session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
    """

    async def create_user(self, user: User) -> User:
        """
        Создает нового пользователя в базе данных.
        Args:
            user (User): Объект пользователя для создания.
        Returns:
            User: Созданный пользователь.
        Raises:
            UserAlreadyExistsException: Если пользователь с таким именем уже существует.
        """
        async with self.session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExistsException
            return user

    async def get_user_by_username(self, username: str) -> User:
        """
        Получает пользователя по его имени пользователя.
        Args:
            username (str): Имя пользователя для поиска.
        Returns:
            User: Найденный пользователь.
        Raises:
            UserNotFoundException: Если пользователь не найден.
        """
        async with self.session as session:
            query = select(User).filter_by(username=username)
            try:
                user_dto = await session.execute(query)
                return user_dto.scalar_one()
            except NoResultFound:
                raise UserNotFoundException
