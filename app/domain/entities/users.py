from dataclasses import dataclass, asdict

from app.domain.entities.base import BaseEntity
from app.domain.values.users import UserName, Password


@dataclass
class User(BaseEntity):
    username: UserName
    password: Password

    def to_dict(self) -> dict:
        return asdict(self)
