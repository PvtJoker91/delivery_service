from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass
class HTTPRequestException(ApplicationException):
    url: str

    @property
    def message(self):
        return f'Произошла ошибка во время выполнения запроса к URL "{self.url}"'
