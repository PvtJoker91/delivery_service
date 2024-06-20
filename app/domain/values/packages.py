from dataclasses import dataclass

from app.domain.exceptions.packages import (
    WrongPriceValueException,
    WrongWeightValueException,
    TitleTooLongException,
    EmptyTitleException
)
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class PackagePrice(BaseValueObject[float]):
    def validate(self):
        if not self.value or self.value < 0:
            raise WrongPriceValueException()

    def as_generic_type(self) -> float:
        return float(self.value)


@dataclass(frozen=True)
class PackageWeight(BaseValueObject[float]):
    def validate(self):
        if not self.value or self.value < 0:
            raise WrongWeightValueException()

    def as_generic_type(self) -> float:
        return float(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyTitleException()

        if len(self.value) > 100:
            raise TitleTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)
