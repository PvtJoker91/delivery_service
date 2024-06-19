from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.users import User as UserEntity
from app.infra.repositories.users.base import BaseUserRepository
from app.infra.repositories.users.converters import convert_user_entity_to_model


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    session: AsyncSession

    async def create_user(self, user: UserEntity) -> UserEntity:
        async with self.session as session:
            user_dto = convert_user_entity_to_model(user)
            try:
                session.add(user_dto)
                await session.commit()
            except Exception as e:
                raise Exception('хуйня с юзер дб')
            return user_dto.to_entity()
