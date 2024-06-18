from dataclasses import dataclass, asdict

from app.domain.entities.base import BaseEntity
from app.domain.values.users import UserName


@dataclass
class User(BaseEntity):
    first_name: UserName
    last_name: UserName

    def to_dict(self) -> dict:
        return asdict(self)
