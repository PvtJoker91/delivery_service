from app.domain.exceptions.base import ApplicationException


class UserAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return 'Пользователь с таким именем уже существует'


class UserNotFoundException(ApplicationException):
    @property
    def message(self):
        return 'Пользователь не существует'
