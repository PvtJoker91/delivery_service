from app.domain.exceptions.base import ApplicationException


class PackageNotFoundException(ApplicationException):
    @property
    def message(self):
        return 'Посылки с таким ID не существует'


class PackageTypeAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return 'Тип посылки с таким названием уже существует'


class PackageTypeNotFoundException(ApplicationException):
    @property
    def message(self):
        return 'Тип посылки с таким ID не существует'
