from app.domain.exceptions.users import EmptyUserNameException, UserNameTooLongException
from app.domain.values.base import BaseValueObject


class UserName(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyUserNameException()

        if len(self.value) > 50:
            raise UserNameTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)


class Password(BaseValueObject[str | bytes]):
    def validate(self):
        if not self.value:
            raise EmptyUserNameException()

        if len(self.value) > 50:
            raise UserNameTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)