import uuid

from app.infra.exceptions.users import UserAlreadyExistsException, UserNotFoundException
from app.infra.db.users import User
from app.infra.repositories.users.base import BaseUserRepository


class MemoryUserRepository(BaseUserRepository):
    saved_users: dict[int: User] = {
        1: User(
            id=1,
            username='user1',
            password=b'$2b$12$T0Eb3Yfp9KcwZiUchYBbr.TbxHbDhgJnrq1EV9/RrFU0dIBbUXJta'
        )
    }

    async def create_user(self, user: User) -> User:
        user.id = int(uuid.uuid4())
        for saved_user in self.saved_users.values():
            if saved_user.username == user.username:
                raise UserAlreadyExistsException
        self.saved_users[user.id] = user
        return user

    async def get_user_by_username(self, username: str) -> User:
        for user in self.saved_users.values():
            if user.username == username:
                return user
        raise UserNotFoundException
