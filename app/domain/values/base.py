from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject[VT](ABC):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def as_generic_type(self) -> VT:
        ...
