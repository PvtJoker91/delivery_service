from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UserNameTooLongException(ApplicationException):
    name: str

    @property
    def message(self):
        return f'Слишком длинное имя/фамилия "{self.name[:50]}..."'


class EmptyUserNameException(ApplicationException):
    @property
    def message(self):
        return 'Имя/фамилия не может быть пустым'
