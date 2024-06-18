from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    title: str

    @property
    def message(self):
        return f'Слишком длинное название "{self.title[:100]}..."'


class EmptyTitleException(ApplicationException):
    @property
    def message(self):
        return 'Название не может быть пустым'


class WrongPriceValueException(ApplicationException):
    @property
    def message(self):
        return 'Неверно указана стоимость содержимого посылки'


class WrongWeightValueException(ApplicationException):
    @property
    def message(self):
        return 'Неверно указан вес посылки'
